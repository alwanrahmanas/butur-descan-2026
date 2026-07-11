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
