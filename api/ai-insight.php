<?php
/**
 * AI Insight Proxy - Desa Cantik
 *
 * Menerima ringkasan data agregat dari frontend, memanggil OpenAI, lalu
 * mengembalikan analisis ringkas. Jangan kirim NIK, KK, nama, alamat, atau HP.
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('Referrer-Policy: strict-origin-when-cross-origin');
header("Content-Security-Policy: default-src 'none'");

$cfg = require __DIR__ . '/config.php';

function json_response(array $payload, int $status = 200): void
{
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

function read_json_file(string $path): array
{
    if (!file_exists($path)) {
        return [];
    }
    $raw = file_get_contents($path);
    $data = json_decode($raw ?: '[]', true);
    return is_array($data) ? $data : [];
}

function write_json_file(string $path, array $data): void
{
    file_put_contents($path, json_encode($data, JSON_UNESCAPED_UNICODE), LOCK_EX);
}

function truthy_count(array $rows, string $key): int
{
    $count = 0;
    foreach ($rows as $row) {
        $value = $row[$key] ?? null;
        if ($value === true || $value === 1 || $value === '1' || $value === 'Ya' || $value === 'ya') {
            $count++;
        }
    }
    return $count;
}

/**
 * Sanitasi input: hapus karakter kontrol dan trim.
 */
function sanitize_input(string $text): string
{
    // Hapus karakter kontrol kecuali newline dan tab
    $text = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', '', $text);
    return trim($text);
}

/**
 * Deteksi pola prompt injection yang umum.
 * Mengembalikan true jika terdeteksi upaya injeksi.
 */
function detect_prompt_injection(string $text): bool
{
    $lower = mb_strtolower($text, 'UTF-8');

    $patterns = [
        // Upaya mengabaikan instruksi sistem
        '/ignore\s+(all\s+)?(previous|above|prior|earlier)\s+(instructions|prompts|rules|context)/i',
        '/forget\s+(all\s+)?(previous|above|prior|earlier)\s+(instructions|prompts|rules|context)/i',
        '/disregard\s+(all\s+)?(previous|above|prior|earlier)\s+(instructions|prompts|rules|context)/i',
        '/abaikan\s+(semua\s+)?(instruksi|aturan|perintah|prompt)\s+(sebelumnya|di\s+atas)/i',
        '/lupakan\s+(semua\s+)?(instruksi|aturan|perintah|prompt)/i',

        // Upaya mengubah peran/identitas
        '/you\s+are\s+now/i',
        '/act\s+as\s+(a|an|if)/i',
        '/pretend\s+(you|to\s+be)/i',
        '/role.?play\s+as/i',
        '/sekarang\s+kamu\s+(adalah|jadi|berperan)/i',
        '/bertindak\s+sebagai/i',
        '/berpura.?pura/i',

        // Upaya mengekstrak system prompt
        '/repeat\s+(the|your)\s+(system|initial|original)\s+(prompt|instructions|message)/i',
        '/what\s+(are|is|were)\s+your\s+(system|initial|original)\s+(prompt|instructions)/i',
        '/show\s+(me\s+)?(the|your)\s+(system|initial|original)\s+(prompt|instructions)/i',
        '/tampilkan\s+(instruksi|prompt|perintah)\s+(sistem|awal)/i',
        '/ulangi\s+(instruksi|prompt|perintah)\s+(sistem|awal)/i',

        // Upaya injeksi format pesan (role injection)
        '/^\s*\[?(system|assistant|admin)\]?\s*:/im',
        '/<\|?(system|im_start|im_end)\|?>/i',
        '/###\s*(system|instruction|assistant)/i',

        // Upaya DAN / jailbreak
        '/\bDAN\b.*mode/i',
        '/developer\s+mode/i',
        '/jailbreak/i',
    ];

    foreach ($patterns as $pattern) {
        if (preg_match($pattern, $text)) {
            return true;
        }
    }

    return false;
}

// CORS for local preview or future production domain.
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$host = $_SERVER['HTTP_HOST'] ?? '';
$originHost = $origin ? parse_url($origin, PHP_URL_HOST) : '';
$allowed = in_array($origin, $cfg['allowed_origins'], true) || ($originHost && $host && $originHost === preg_replace('/:\d+$/', '', $host));
if ($origin && !$allowed) {
    json_response(['success' => false, 'error' => 'Origin tidak diizinkan.'], 403);
}
if ($origin) {
    header("Access-Control-Allow-Origin: $origin");
    header('Vary: Origin');
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    json_response(['success' => false, 'error' => 'Method not allowed.'], 405);
}

$input = json_decode(file_get_contents('php://input') ?: '{}', true);
if (!is_array($input)) {
    json_response(['success' => false, 'error' => 'Payload tidak valid.'], 400);
}

$context = sanitize_input((string)($input['context'] ?? ''));

$profiles = require __DIR__ . '/village-profiles.php';
if (preg_match('/Wilayah:\s*(Desa\s+[a-zA-Z\s]+)/i', $context, $matches)) {
    $villageName = trim($matches[1]);
    if (isset($profiles[$villageName])) {
        $p = $profiles[$villageName];
        $villageContext = "PROFIL LOKASI:\n- Nama: {$p['nama_resmi']}\n- Lokasi: Kec. {$p['kecamatan']}, Kab. {$p['kabupaten']}, {$p['provinsi']}\n- Tipologi: {$p['tipologi']}\n- Potensi: {$p['potensi']}\n- Akses: {$p['aksesibilitas']}\n\n";
        $context = $villageContext . $context;
    }
}
$mode = preg_replace('/[^a-z_-]/', '', strtolower((string)($input['mode'] ?? 'insight')));
$question = sanitize_input((string)($input['question'] ?? ''));
$history = is_array($input['history'] ?? null) ? $input['history'] : [];
$allowedModes = ['insight', 'laporan', 'prioritas', 'chat'];
if (!in_array($mode, $allowedModes, true)) {
    $mode = 'insight';
}

if ($context === '' || strlen($context) > 12000) {
    json_response(['success' => false, 'error' => 'Data agregat tidak valid.'], 400);
}
if ($mode === 'chat' && ($question === '' || strlen($question) > 700)) {
    json_response(['success' => false, 'error' => 'Pertanyaan tidak valid atau terlalu panjang.'], 400);
}

// Deteksi prompt injection pada input pengguna
if (detect_prompt_injection($question) || detect_prompt_injection($context)) {
    json_response([
        'success' => false,
        'error' => 'Pertanyaan Anda terdeteksi mengandung pola yang tidak diizinkan. Silakan ajukan pertanyaan seputar data desa.',
    ], 400);
}

$safeHistory = [];
foreach (array_slice($history, -4) as $item) {
    $role = ($item['role'] ?? '') === 'assistant' ? 'assistant' : 'user';
    $content = trim((string)($item['content'] ?? ''));
    if ($content !== '') {
        $safeHistory[] = [
            'role' => $role,
            'content' => substr($content, 0, 500),
        ];
    }
}

$cacheKey = hash('sha256', $mode . "\n" . $context . "\n" . $question . "\n" . json_encode($safeHistory, JSON_UNESCAPED_UNICODE));
$cache = read_json_file($cfg['cache_file']);
$now = time();
if (isset($cache[$cacheKey]) && (($now - ($cache[$cacheKey]['time'] ?? 0)) < $cfg['cache_ttl_seconds'])) {
    json_response([
        'success' => true,
        'analysis' => $cache[$cacheKey]['analysis'],
        'cached' => true,
    ]);
}

if (!$cfg['openai_api_key']) {
    json_response([
        'success' => false,
        'error' => 'OPENAI_API_KEY belum dikonfigurasi di server hosting.',
    ], 500);
}

// Rate limiting only for calls that would hit OpenAI.
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$rates = read_json_file($cfg['rate_limit_file']);
foreach ($rates as $key => $timestamps) {
    $rates[$key] = array_values(array_filter((array)$timestamps, fn($t) => ($now - (int)$t) < 3600));
    if (!$rates[$key]) {
        unset($rates[$key]);
    }
}
$myRequests = $rates[$ip] ?? [];
if (count($myRequests) >= $cfg['rate_limit_max']) {
    json_response(['success' => false, 'error' => 'Batas penggunaan tercapai. Coba lagi dalam 1 jam.'], 429);
}

$modeInstruction = [
    'insight' => 'Buat analisis dashboard yang singkat, mudah dipahami, dan langsung berguna.',
    'laporan' => 'Buat narasi laporan resmi yang siap ditempel ke dokumen paparan desa.',
    'prioritas' => 'Fokus pada prioritas program: urutkan 3 masalah utama dan 3 aksi paling realistis.',
    'chat' => 'Jawab pertanyaan pengguna secara ringkas, praktis, dan hanya berdasarkan data agregat dashboard.',
][$mode];

$systemPrompt = $mode === 'chat' ? <<<PROMPT
Anda adalah analis statistik untuk dashboard Desa Cantik BPS.
Jawab hanya berdasarkan data agregat yang diberikan. Jangan mengarang angka, nama, NIK, alamat, atau data keluarga tertentu.
Jika pertanyaan butuh data yang tidak tersedia dalam agregat, jelaskan keterbatasannya dan beri cara membaca data yang tersedia.
Bahasa Indonesia formal, sederhana, dan mudah dipahami pemerintah desa.
Jawaban maksimal 2 paragraf pendek atau 5 bullet.
Jangan mengulang format Ringkasan, Temuan Utama, Rekomendasi Praktis, atau Catatan Kehati-hatian kecuali pengguna memintanya.
Jika pengguna hanya menyapa, balas sapaan singkat dan tawarkan contoh pertanyaan tentang data.
Jawab pertanyaan terakhir secara langsung.
Jangan menyebut diri sebagai AI.

ATURAN KETAT (WAJIB DIPATUHI):
- Anda HANYA boleh menjawab pertanyaan yang berkaitan dengan data statistik desa, demografi, perumahan, kesehatan, pendidikan, pekerjaan, dan program bantuan sosial yang ada di dashboard.
- Jika pengguna bertanya di luar topik data desa (misalnya: menulis kode program, cerita fiksi, resep masakan, matematika umum, pengetahuan umum, terjemahan bahasa asing, atau topik apa pun yang tidak berkaitan dengan data agregat desa), TOLAK dengan sopan.
- Contoh penolakan: "Maaf, saya hanya bisa membantu menganalisis data statistik desa yang tersedia di dashboard ini. Silakan ajukan pertanyaan seputar data demografi, perumahan, kesehatan, atau program bantuan sosial desa."
- JANGAN PERNAH menulis kode program dalam bahasa apa pun (Python, Rust, JavaScript, dll.).
- JANGAN PERNAH menjawab pertanyaan yang tidak ada kaitannya dengan data desa, meskipun pengguna memaksa.
PROMPT
:
<<<PROMPT
Anda adalah analis statistik senior untuk program Desa Cantik BPS.
Analisis hanya berdasarkan data agregat yang diberikan. Jangan mengarang angka.
Bahasa Indonesia formal, sederhana, dan mudah dipahami pemerintah desa.

Format jawaban:
## Ringkasan
2 paragraf pendek.

## Temuan Utama
- 3 sampai 5 bullet.

## Rekomendasi Praktis
- 3 sampai 5 bullet yang spesifik dan bisa dikerjakan.

## Catatan Kehati-hatian
1 kalimat tentang keterbatasan data.

Jangan menyebut diri sebagai AI.

ATURAN KETAT: Anda HANYA boleh menganalisis data statistik desa. Jangan menjawab pertanyaan di luar konteks data desa. Jangan menulis kode program. Jika diminta hal di luar topik, tolak dengan sopan dan arahkan kembali ke analisis data desa.
PROMPT;

$messages = [
    ['role' => 'system', 'content' => $systemPrompt],
    ['role' => 'user', 'content' => "$modeInstruction\n\nData agregat dashboard:\n\n$context"],
];
if ($mode === 'chat') {
    foreach ($safeHistory as $item) {
        $messages[] = $item;
    }
    // Bungkus pertanyaan dengan delimiter agar tidak diinterpretasi sebagai instruksi
    $messages[] = ['role' => 'user', 'content' => "Pertanyaan pengguna (jawab HANYA berdasarkan data desa):\n<<<USER_QUESTION>>>\n$question\n<<<END_USER_QUESTION>>>"];
    // Sandwich defense: ulangi guardrail di akhir
    $messages[] = ['role' => 'system', 'content' => 'PENGINGAT: Anda HANYA boleh menjawab berdasarkan data agregat desa di atas. JANGAN pernah menulis kode, cerita fiksi, atau menjawab di luar topik statistik desa. Jika pertanyaan di atas tidak relevan dengan data desa, tolak dengan sopan.'];
}

$payload = json_encode([
    'model' => $cfg['openai_model'],
    'max_completion_tokens' => $mode === 'chat' ? min(650, $cfg['max_completion_tokens']) : $cfg['max_completion_tokens'],
    'messages' => $messages,
], JSON_UNESCAPED_UNICODE);

if (!function_exists('curl_init')) {
    json_response([
        'success' => false,
        'error' => 'Ekstensi PHP cURL belum aktif di server. Aktifkan extension=curl lalu restart Laragon.',
    ], 500);
}

$ch = curl_init('https://api.openai.com/v1/chat/completions');
$isLocalServer = in_array($_SERVER['SERVER_NAME'] ?? '', ['localhost', '127.0.0.1']) || substr($_SERVER['SERVER_NAME'] ?? '', -5) === '.test';

curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_CONNECTTIMEOUT => 20,
    CURLOPT_TIMEOUT => 120,
    CURLOPT_SSL_VERIFYPEER => !$isLocalServer,
    CURLOPT_POSTFIELDS => $payload,
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $cfg['openai_api_key'],
    ],
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlErr = curl_error($ch);
curl_close($ch);

if ($curlErr) {
    // Jangan bocorkan detail internal cURL ke pengguna
    error_log('AI Insight cURL error: ' . $curlErr);
    json_response(['success' => false, 'error' => 'Gagal menghubungi layanan AI. Silakan coba lagi nanti.'], 502);
}

$data = json_decode($response ?: '{}', true);
$analysis = $data['choices'][0]['message']['content'] ?? '';
if ($httpCode < 200 || $httpCode >= 300 || !$analysis) {
    // Log detail error untuk debugging, tapi jangan bocorkan ke pengguna
    $internalErr = $data['error']['message'] ?? 'unknown';
    error_log("AI Insight API error (HTTP $httpCode): $internalErr");
    json_response(['success' => false, 'error' => 'Layanan AI sedang tidak tersedia. Silakan coba lagi nanti.'], 502);
}

$rates[$ip][] = $now;
write_json_file($cfg['rate_limit_file'], $rates);

$cache[$cacheKey] = [
    'time' => $now,
    'analysis' => $analysis,
];
if (count($cache) > 50) {
    uasort($cache, fn($a, $b) => ($b['time'] ?? 0) <=> ($a['time'] ?? 0));
    $cache = array_slice($cache, 0, 50, true);
}
write_json_file($cfg['cache_file'], $cache);

json_response([
    'success' => true,
    'analysis' => $analysis,
    'cached' => false,
]);
