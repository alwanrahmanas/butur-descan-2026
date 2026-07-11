<?php
/**
 * Konfigurasi API - Desa Cantik
 *
 * Simpan API key di environment variable OPENAI_API_KEY.
 * Contoh pada hosting Apache: SetEnv OPENAI_API_KEY "sk-..."
 */

return [
    'openai_api_key' => getenv('OPENAI_API_KEY') ?: '',
    'openai_model' => getenv('OPENAI_MODEL') ?: 'gpt-5.4-mini-2026-03-17',
    'max_completion_tokens' => 500,

    // Google Sheets Proxy Config
    'sheet_ids' => [
        'desa-laangke' => getenv('SHEET_ID_LAANGKE') ?: '1FZZpyF6lG6cvPUu-i8gn9WcOMhExN_OG',
        'kelurahan-lakonea' => getenv('SHEET_ID_LAKONEA') ?: '1jjnaeoxpSVPY3Rl1aMbFlkzsgDo832h8',
        'desa-malalanda' => getenv('SHEET_ID_MALALANDA') ?: '1_eRZFFXR67qRl7nzZ8lSe7d5Tp88xnEe',
        'popup' => getenv('SHEET_ID_POPUP') ?: '1DlOHH6M3QiEot8Jv_ik-XUIpCx9Q-BzJJVo3H8UB6pI',
    ],
    
    // Proxy Cache Config (untuk CSV Google Sheets)
    'proxy_cache_dir' => __DIR__ . '/cache',
    'proxy_cache_ttl' => 300, // 5 menit

    // Maksimal request AI non-cache per IP per jam (Ditingkatkan untuk kemudahan testing).
    'rate_limit_max' => 10,
    'rate_limit_file' => __DIR__ . '/.rate_limits.json',

    // Cache jawaban agar hemat biaya API untuk data yang sama.
    'cache_ttl_seconds' => 86400,
    'cache_file' => __DIR__ . '/.ai_cache.json',

    // Tambahkan domain produksi di sini setelah hosting aktif.
    'allowed_origins' => [
        'http://127.0.0.1:5500',
        'http://localhost:5500',
        'http://localhost',
        'http://127.0.0.1',
        'https://buton-utara.net',
        'https://www.buton-utara.net',
        'https://laangke.buton-utara.net',
        'https://lakonea.buton-utara.net',
        'https://malalanda.buton-utara.net',
    ],
];
