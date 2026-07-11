<?php
/**
 * Proxy Data - Mengambil data CSV dari Google Sheets secara rahasia.
 * Endpoint ini melindungi Spreadsheet ID agar tidak terekspos ke frontend.
 */
header('Content-Type: text/csv; charset=utf-8');

// Header CORS sederhana (jika diperlukan)
header('Access-Control-Allow-Origin: *');

$config = require __DIR__ . '/config.php';

$lokus = $_GET['lokus'] ?? '';
$type = $_GET['type'] ?? '';
$gid = $_GET['gid'] ?? '';

// 1. Tentukan SPREADSHEET_ID
$spreadsheet_id = '';
if ($type === 'popup') {
    $spreadsheet_id = $config['sheet_ids']['popup'] ?? '';
} else {
    // Validasi lokus
    if (!isset($config['sheet_ids'][$lokus])) {
        http_response_code(400);
        echo "Error: Lokus tidak valid.";
        exit;
    }
    $spreadsheet_id = $config['sheet_ids'][$lokus];
    
    // Validasi GID (hanya angka) mencegah injeksi cURL
    if (empty($gid) || !ctype_digit((string)$gid)) {
        http_response_code(400);
        echo "Error: GID tidak valid (harus angka).";
        exit;
    }
}

if (empty($spreadsheet_id)) {
    http_response_code(500);
    echo "Error: Spreadsheet ID tidak dikonfigurasi.";
    exit;
}

// 2. Caching
$cache_dir = $config['proxy_cache_dir'];
if (!is_dir($cache_dir)) {
    mkdir($cache_dir, 0755, true);
}

$cache_key = md5($spreadsheet_id . '_' . $gid);
$cache_file = $cache_dir . '/' . $cache_key . '.csv';

// Jika cache masih valid, gunakan cache
if (file_exists($cache_file) && (time() - filemtime($cache_file) < $config['proxy_cache_ttl'])) {
    readfile($cache_file);
    exit;
}

// 3. Bangun URL Download
if ($type === 'popup') {
    $url = "https://docs.google.com/spreadsheets/d/{$spreadsheet_id}/export?format=csv";
} else {
    $url = "https://docs.google.com/spreadsheets/d/{$spreadsheet_id}/export?format=csv&gid={$gid}";
}

// 4. Proses cURL ke Google Sheets
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
// Timeout untuk mencegah connection hang
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
// Tetap nyalakan SSL Verify Peer untuk keamanan
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);

$csv_data = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curl_error = curl_error($ch);
curl_close($ch);

// 5. Error Handling
if ($csv_data === false) {
    http_response_code(500);
    echo "Error: Gagal mengambil data (cURL Error: $curl_error).";
    exit;
}

if ($http_code !== 200) {
    http_response_code($http_code);
    echo "Error: Google Sheets mengembalikan status $http_code. (Pastikan sheet di-publish/Anyone with the link can view).";
    exit;
}

// 6. Simpan Cache & Tampilkan
file_put_contents($cache_file, $csv_data);
echo $csv_data;
