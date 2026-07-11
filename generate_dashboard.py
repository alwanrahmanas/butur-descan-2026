#!/usr/bin/env python3
"""
Generator Dashboard Desa Cantik — Format Template Rapih
Membaca CSS dari file existing, menggabungkan dengan body/JS baru,
dan menghasilkan 3 file index.html untuk setiap desa.
"""
import os

# ─── KONFIGURASI DESA ─────────────────────────────────────────────
VILLAGES = [
    {
        'dir': 'Laangke',
        'name': 'Desa Laangke',
        'id': 'desa-laangke',
        'lokus_js': '["Desa Laangke"]',
        'spreadsheet_id': '1FZZpyF6lG6cvPUu-i8gn9WcOMhExN_OG',
        'sheet_keluarga': 'Entri_Keluarga',
        'gids': {
            'keluarga': '1804314654',
            'lapangan': '1446044024',
            'pendidikan': '1505151008',
            'kesehatan': '2132676905',
            'agama': '87680082',
            'disabilitas': '1083717073',
            'foto': ''
        }
    },
    {
        'dir': 'Lakonea',
        'name': 'Kelurahan Lakonea',
        'id': 'kelurahan-lakonea',
        'lokus_js': '["Kelurahan Lakonea"]',
        'spreadsheet_id': '1jjnaeoxpSVPY3Rl1aMbFlkzsgDo832h8',
        'sheet_keluarga': 'Entri_Keluarga_Lakonea',
        'gids': {
            'keluarga': '1124726980',
            'lapangan': '821191437',
            'pendidikan': '525501546',
            'kesehatan': '161083327',
            'agama': '114526696',
            'disabilitas': '1602534448',
            'foto': ''
        }
    },
    {
        'dir': 'Malalanda',
        'name': 'Desa Malalanda',
        'id': 'desa-malalanda',
        'lokus_js': '["Desa Malalanda"]',
        'spreadsheet_id': '1_eRZFFXR67qRl7nzZ8lSe7d5Tp88xnEe',
        'sheet_keluarga': 'Entri_Keluarga',
        'gids': {
            'keluarga': '515567017',
            'lapangan': '842096498',
            'pendidikan': '455951459',
            'kesehatan': '622379610',
            'agama': '866475550',
            'disabilitas': '638945844',
            'foto': ''
        }
    },
]

# ─── 1. BACA CSS/HEAD DARI FILE EXISTING ──────────────────────────
print("Membaca CSS dari Laangke/index.html...")
with open('Laangke/index.html', 'r', encoding='utf-8') as f:
    existing = f.read()

# Ambil dari awal sampai </head>
head_end_idx = existing.index('</head>') + len('</head>')
head_section = existing[:head_end_idx]

# ─── 2. TEMPLATE BODY HTML ───────────────────────────────────────
def get_body_html(v):
    return f'''

<body>

    <!-- Header -->
    <header>
        <div class="container nav-container">
            <a href="#" class="logo">
                <svg viewBox="0 0 100 100" width="32" height="32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100" height="100" rx="20" fill="currentColor" fill-opacity="0.1" />
                    <path d="M50 20L20 45V80H40V60H60V80H80V45L50 20Z" fill="currentColor" />
                    <circle cx="50" cy="45" r="8" fill="var(--color-surface)" />
                </svg>
                Desa Cantik
            </a>
            <div class="nav-links" id="navLinks">
                <a href="#beranda">Beranda</a>
                <a href="#profil">Profil Lokus</a>
                <a href="#dashboard-keluarga">Keluarga</a>
                <a href="#dashboard-sosial">Sosial &amp; Budaya</a>
                <a href="#unduh-data">Unduh Data</a>
                <a href="#tentang-data">Tentang</a>
            </div>
            <div class="nav-actions">
                <button class="theme-toggle" id="themeToggle" aria-label="Toggle Dark Mode"><i data-lucide="moon"
                        id="themeIcon"></i></button>
                <button class="menu-toggle" id="menuToggle" aria-label="Menu"><i data-lucide="menu"></i></button>
            </div>
        </div>
    </header>

    <main>
        <!-- Beranda -->
        <section id="beranda" class="hero">
            <div class="container">
                <div class="hero-content">
                    <div class="hero-copy">
                        <div class="hero-eyebrow"><i data-lucide="users-round"></i> Dashboard Profil Keluarga</div>
                        <h1>Desa Cantik<br>{v['name']}</h1>
                        <p>Dashboard statistik berbasis <strong>Profil Keluarga SDGs Desa</strong> untuk
                            {v['name']} — Kuesioner SDGSDES.26 Tahun 2026.</p>
                        <div class="hero-cta">
                            <a href="#dashboard-keluarga" class="btn btn-primary"><i data-lucide="layout-dashboard"></i>
                                Dashboard Keluarga</a>
                            <a href="#dashboard-sosial" class="btn btn-secondary"><i data-lucide="landmark"></i> Sosial
                                &amp; Budaya</a>
                        </div>
                    </div>
                    <aside class="hero-panel" aria-label="Ringkasan data keluarga">
                        <div class="hero-panel-header">
                            <h2 class="hero-panel-title">Ringkasan Dataset</h2>
                            <span class="hero-panel-chip"><i data-lucide="database"></i> Data aktif</span>
                        </div>
                        <div class="metric-strip">
                            <div class="metric-tile"><span>Lokus</span><strong id="metricLokus">1</strong></div>
                            <div class="metric-tile"><span>Sumber</span><strong>Sheet</strong></div>
                            <div class="metric-tile"><span>Status</span><strong>Aktif</strong></div>
                            <div class="metric-tile"><span>Tahun</span><strong>2026</strong></div>
                        </div>
                    </aside>
                </div>
                <div class="lokus-grid" id="berandaLokusGrid"></div>
            </div>
        </section>

        <!-- Profil Lokus -->
        <section id="profil" class="section">
            <div class="container">
                <h2 class="section-title">Profil Lokus Program</h2>
                <p class="section-desc">Karakteristik demografi dan permukiman wilayah percontohan.</p>
                <div class="tabs" id="profilTabs"><button class="tab-btn active"
                        data-target="profil-{v['id']}">{v['name']}</button></div>
                <div id="profilContentContainer"></div>
            </div>
        </section>

        <!-- Dashboard Keluarga -->
        <section id="dashboard-keluarga" class="section" style="padding-top: 2rem;">
            <div class="container">
                <h2 class="section-title" style="text-align: left;">Dashboard Keluarga</h2>
                <div class="kpi-grid" id="kpiKeluarga"></div>
                <div class="charts-grid">
                    <div class="chart-card">
                        <h3 class="chart-title">Status Tempat Tinggal</h3>
                        <div class="chart-container"><canvas id="chartTinggal"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Penerima Program Bantuan</h3>
                        <div class="chart-container"><canvas id="chartBantuan"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Jenis Lantai Rumah</h3>
                        <div class="chart-container"><canvas id="chartLantai"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Jenis Dinding Rumah</h3>
                        <div class="chart-container"><canvas id="chartDinding"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Jenis Atap Rumah</h3>
                        <div class="chart-container"><canvas id="chartAtap"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Sumber Penerangan</h3>
                        <div class="chart-container"><canvas id="chartPenerangan"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Sumber Air Minum</h3>
                        <div class="chart-container"><canvas id="chartAirMinum"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Fasilitas Buang Air Besar</h3>
                        <div class="chart-container"><canvas id="chartBAB"></canvas></div>
                    </div>
                    <div class="chart-card chart-full">
                        <h3 class="chart-title">Bahan Bakar Memasak</h3>
                        <div class="chart-container" style="height: 250px;"><canvas id="chartEnergi"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Tempat Buang Sampah</h3>
                        <div class="chart-container"><canvas id="chartSampah"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Pembuangan Akhir Tinja</h3>
                        <div class="chart-container"><canvas id="chartTinja"></canvas></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Dashboard Sosial, Budaya & Ketenagakerjaan -->
        <section id="dashboard-sosial" class="section" style="background-color: var(--color-surface-2);">
            <div class="container">
                <h2 class="section-title" style="text-align: left;">Dashboard Sosial, Budaya &amp; Ketenagakerjaan</h2>
                <div class="kpi-grid" id="kpiSosial"></div>
                <div class="charts-grid">
                    <div class="chart-card chart-full">
                        <h3 class="chart-title">Sumber Penghasilan Utama (R403)</h3>
                        <div class="chart-container" style="height: 380px;"><canvas id="chartLapanganUsaha"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Agama / Kepercayaan (R701)</h3>
                        <div class="chart-container"><canvas id="chartAgama"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Penyandang Disabilitas (R702)</h3>
                        <div class="chart-container"><canvas id="chartDisabilitas"></canvas></div>
                    </div>
                </div>
                <h3 style="font-size: 1.25rem; font-weight: 800; margin: 2.5rem 0 1rem; display: none;">Akses Sarana Pendidikan per SLS
                    (R601)</h3>
                <div class="table-container" id="tabelPendidikan" style="display: none;"></div>
                <h3 style="font-size: 1.25rem; font-weight: 800; margin: 2.5rem 0 1rem; display: none;">Akses Sarana Kesehatan per SLS
                    (R602)</h3>
                <div class="table-container" id="tabelKesehatan" style="display: none;"></div>
            </div>
        </section>

        <!-- Unduh Data Agregat -->
        <section id="unduh-data" class="section">
            <div class="container">
                <h2 class="section-title">Unduh Data Agregat</h2>
                <p class="section-desc">Unduh data yang ditampilkan di dashboard dalam format Excel. <strong>Tidak
                        mengandung identitas personal</strong> (NIK, KK, nama, alamat, No. HP).</p>
                <div class="download-grid">
                    <div class="download-card">
                        <i data-lucide="home"></i>
                        <h3>Tabel Keluarga</h3>
                        <p class="text-muted text-sm" style="margin-bottom: 1.5rem;">Status rumah, atap, dinding, lantai,
                            energi, air minum, bantuan sosial</p>
                        <button class="btn btn-secondary" style="width:100%" onclick="exportAgregat('keluarga')">Unduh
                            Tabel Keluarga</button>
                    </div>
                    <div class="download-card">
                        <i data-lucide="landmark"></i>
                        <h3>Tabel Sosial</h3>
                        <p class="text-muted text-sm" style="margin-bottom: 1.5rem;">Lapangan usaha, agama, disabilitas,
                            akses pendidikan &amp; kesehatan</p>
                        <button class="btn btn-secondary" style="width:100%" onclick="exportAgregat('sosial')">Unduh
                            Tabel Sosial</button>
                    </div>
                    <div class="download-card">
                        <i data-lucide="folder-archive"></i>
                        <h3>Gabungan</h3>
                        <p class="text-muted text-sm" style="margin-bottom: 1.5rem;">Kedua tabel di atas dalam satu
                            workbook Excel</p>
                        <button class="btn btn-primary" style="width:100%" onclick="exportAgregat('gabungan')">Unduh
                            Gabungan (.xlsx)</button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Tentang Data -->
        <section id="tentang-data" class="section" style="background-color: var(--color-surface-2);">
            <div class="container" style="max-width: 800px;">
                <h2 class="section-title">Tentang Data</h2>
                <div
                    style="background: var(--color-surface); padding: 2rem; border-radius: var(--radius-lg); border: 1px solid var(--color-border);">
                    <p style="margin-bottom: 1rem;">Website ini merupakan dashboard untuk program <strong>Desa
                            Cantik (Cinta Statistik)</strong> Kabupaten Buton Utara, yang dibangun sesuai instrumen
                        <strong>SDGSDES.26 — Kuesioner Profil Keluarga</strong> (Template Rapih 2026).</p>
                    <ul
                        style="list-style: disc; padding-left: 1.5rem; color: var(--color-text-muted); display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem;">
                        <li><strong>Sumber Struktur:</strong> Kuesioner Profil Keluarga SDGSDES.26 (Revisi 2026).</li>
                        <li><strong>Unit Observasi:</strong> Keluarga/Rumah Tangga (Entri_Keluarga).</li>
                        <li><strong>Sheet Tambahan:</strong> R403 Lapangan Usaha, R601 Pendidikan SLS, R602 Kesehatan SLS,
                            R701 Agama, R702 Disabilitas.</li>
                        <li><strong>Blok Variabel:</strong> Keterangan Tempat, Kependudukan, Perumahan &amp; Lingkungan,
                            Sosial Budaya, Perlindungan Sosial.</li>
                        <li><strong>Program Bantuan:</strong> BLT Desa, PKH, BPJS PBI, Bantuan Pangan (Bapanas),
                            BNPT/Sembako, PIP, MBG.</li>
                        <li><strong>Status Data:</strong> Data agregat operasional dari sumber data yang terhubung.</li>
                        <li><strong>Integrasi:</strong> Terhubung secara real-time dengan Google Sheets (format Template
                            Rapih).</li>
                    </ul>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer id="kontak">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <div class="logo" style="margin-bottom: 1rem;">
                        <svg viewBox="0 0 100 100" width="24" height="24" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <rect width="100" height="100" rx="20" fill="currentColor" fill-opacity="0.1" />
                            <path d="M50 20L20 45V80H40V60H60V80H80V45L50 20Z" fill="currentColor" />
                            <circle cx="50" cy="45" r="8" fill="var(--color-surface)" />
                        </svg>
                        Desa Cantik
                    </div>
                    <p>Program Pembinaan Statistik Desa Kabupaten Buton Utara.</p>
                </div>
                <div class="footer-col">
                    <h4>Kontak</h4>
                    <p><i data-lucide="map-pin"
                            style="width:16px;height:16px;display:inline-block;vertical-align:text-bottom;"></i> Jl.
                        Statistik No. 1, Buton Utara</p>
                    <p><i data-lucide="mail"
                            style="width:16px;height:16px;display:inline-block;vertical-align:text-bottom;"></i>
                        bps7405@bps.go.id</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>Sistem Dashboard Desa Cantik &copy; 2026 BPS Kabupaten Buton Utara. Hanya data agregat yang
                    ditampilkan.</p>
            </div>
        </div>
    </footer>

    <!-- Photo Popup -->
    <div class="site-popup-overlay" id="photoPopupOverlay" onclick="closePhotoPopup()">
        <div class="site-popup-modal" onclick="event.stopPropagation()" style="max-width:900px;width:95vw;">
            <button class="site-popup-close" onclick="closePhotoPopup()"><i data-lucide="x"
                    style="width:18px;height:18px;"></i></button>
            <iframe id="photoPopupIframe" src="" style="width:100%;height:70vh;border:none;border-radius:8px;background:var(--color-surface-2);" allow="autoplay"></iframe>
        </div>
    </div>

    <!-- AI Insight FAB -->
    <button class="ai-fab" id="aiFab" onclick="openAiInsight()">
        <i data-lucide="sparkles"></i><span>AI Insight</span>
    </button>

    <!-- AI Modal -->
    <div class="ai-overlay" id="aiOverlay">
        <div class="ai-modal">
            <div class="ai-modal-head">
                <h3><i data-lucide="sparkles"></i> AI Insight</h3>
                <button class="ai-close" onclick="closeAiModal()"><i data-lucide="x"
                        style="width:20px;height:20px;"></i></button>
            </div>
            <div class="ai-modal-body" id="aiBody"></div>
            <div class="ai-modal-foot" id="aiFoot" style="display:none;">
                <form class="ai-chat-form" onsubmit="askAiQuestion(event)">
                    <input class="ai-chat-input" id="aiQuestion" type="text"
                        placeholder="Tanya lanjutan tentang data ini..." maxlength="700" autocomplete="off">
                    <button class="ai-chat-send" id="aiSend" type="submit"><i data-lucide="send"
                            style="width:18px;height:18px;"></i></button>
                </form>
                <div class="ai-foot-note">
                    <span>Data dikirim ke AI hanya berupa ringkasan agregat, tanpa identitas personal.</span>
                    <button class="ai-copy-btn" onclick="copyAiResult()"><i data-lucide="copy"
                            style="width:14px;height:14px;"></i> Salin</button>
                </div>
            </div>
        </div>
    </div>
'''


# ─── 3. TEMPLATE JAVASCRIPT ──────────────────────────────────────
def get_js(v):
    return '''
    <script>
        // ══════════════════════════════════════════════════════════════
        //  DASHBOARD DESA CANTIK — FORMAT TEMPLATE RAPIH SDGSDES.26
        //  Auto-generated by generate_dashboard.py
        // ══════════════════════════════════════════════════════════════

        // --- 1. DATA & CONFIG ---
        let dataKeluarga = [];
        let dataLapangan = [];
        let dataAgama = [];
        let dataDisabilitas = [];
        let dataPendidikanSLS = [];
        let dataKesehatanSLS = [];
        let dataFoto = {};

        const USE_LOCAL_XLSX = false;
        const LOCAL_XLSX_PATH = 'data.xlsx';

        const SPREADSHEET_ID = "''' + v['spreadsheet_id'] + '''";
        const SHEET_GIDS = {
            keluarga: "''' + v['gids']['keluarga'] + '''",
            lapangan: "''' + v['gids']['lapangan'] + '''",
            pendidikan: "''' + v['gids']['pendidikan'] + '''",
            kesehatan: "''' + v['gids']['kesehatan'] + '''",
            agama: "''' + v['gids']['agama'] + '''",
            disabilitas: "''' + v['gids']['disabilitas'] + '''",
            foto: "''' + v['gids']['foto'] + '''"
        };
        const POPUP_SPREADSHEET_ID = '1DlOHH6M3QiEot8Jv_ik-XUIpCx9Q-BzJJVo3H8UB6pI';

        const lokusList = ''' + v['lokus_js'] + ''';

        // ── HEADER_TO_VAR — Map descriptive column headers → variable names ──
        const HEADER_TO_VAR = {
            'ID unik keluarga/kuesioner': 'id_keluarga',
            'Provinsi': 'provinsi',
            'Kabupaten': 'kabupaten',
            'Kecamatan': 'kecamatan',
            'Desa/Kelurahan': 'desa_kelurahan',
            'Satuan Lingkungan Setempat (SLS)': 'sls',
            'Nama responden': 'nama_responden',
            'Alamat': 'alamat',
            'No HP responden': 'no_hp_responden',
            'Nama pendata': 'nama_pendata',
            'No HP pendata': 'no_hp_pendata',
            'Tanggal kunjungan': 'tanggal_kunjungan',
            'Nomor KK': 'nomor_kk',
            'Nama kepala keluarga': 'nama_kepala_keluarga',
            'Jumlah anggota keluarga': 'jumlah_art',
            'Jumlah penduduk lansia (60+)': 'jumlah_lansia',
            'Keberadaan ART pekerja migran/TKI': 'pekerja_migran_status',
            'Jumlah pekerja migran laki-laki': 'pekerja_migran_lk',
            'Jumlah pekerja migran perempuan': 'pekerja_migran_pr',
            'Status bangunan tempat tinggal': 'status_bangunan_tinggal',
            'Jenis bukti kepemilikan tanah jika milik sendiri': 'bukti_kepemilikan_tanah',
            'Luas lantai tempat tinggal (m2)': 'luas_lantai',
            'Luas lahan tempat tinggal (m2)': 'luas_lahan',
            'Bahan bangunan utama atap terluas': 'atap_utama',
            'Bahan bangunan utama dinding terluas': 'dinding_utama',
            'Bahan bangunan utama lantai terluas': 'lantai_utama',
            'Fasilitas tempat buang air besar': 'fasilitas_bab',
            'Jenis kloset jika R506a = 1, 2, atau 3': 'jenis_kloset',
            'Tempat pembuangan akhir tinja': 'pembuangan_akhir_tinja',
            'Jenis bahan bakar memasak': 'bahan_bakar_memasak',
            'Tuliskan jika 507 = Lainnya': 'bahan_bakar_lainnya',
            'Sumber utama penerangan rumah': 'sumber_penerangan',
            'Tempat buang sampah utama keluarga': 'tempat_buang_sampah',
            'Tuliskan jika 509 = Lainnya': 'buang_sampah_lainnya',
            'Sumber air utama untuk minum': 'sumber_air_minum',
            'Tuliskan jika 510a = Lainnya': 'air_minum_lainnya',
            'Sumber air untuk mandi/cuci': 'sumber_air_mandi_cuci',
            'Tuliskan jika 510b = Lainnya': 'air_mandi_lainnya',
            'BLT Desa': 'blt_desa',
            'Program Keluarga Harapan (PKH)': 'pkh',
            'BPJS PBI': 'bpjs_pbi',
            'Bantuan pangan pemerintah/Bapanas': 'bantuan_pangan_pemerintah',
            'Program BNPT/Sembako sesuai PDF': 'bnpt_sembako',
            'Program Indonesia Pintar (PIP)': 'pip',
            'Program Makan Bergizi Gratis (MBG)': 'mbg',
            'Ada ART yang sebelumnya menerima bansos namun saat ini tidak menerima': 'pernah_terima_bansos_tidak_lagi_status',
            'Jika 802 = Ada, jumlah orang': 'jumlah_tidak_lagi_menerima',
            'Catatan dari kuesioner': 'catatan',
            // 403_Lapangan
            'ID keluarga sesuai Entri_Keluarga': 'id_keluarga_ref',
            // 701, 702 also use 'Nomor KK' (already mapped)
            // Foto sheet
            'File ID Google Drive': 'foto_file_id',
            'Keterangan': 'foto_keterangan',
        };

        // ── KODE_LOOKUP — Decode kode numerik → label teks ──
        const KODE_LOOKUP = {
            pekerja_migran_status: { 1:"Ada", 2:"Tidak ada" },
            status_bangunan_tinggal: { 1:"Milik Sendiri", 2:"Kontrak/Sewa", 3:"Bebas sewa", 4:"Dinas", 5:"Lainnya" },
            bukti_kepemilikan_tanah: { 1:"SHM atas nama ART", 2:"SHM bukan atas nama ART", 3:"SHM bukan atas nama ART tanpa perjanjian tertulis", 4:"Sertifikat selain SHM", 5:"Surat bukti lainnya", 6:"Tidak punya" },
            atap_utama: { 1:"Beton", 2:"Genteng", 3:"Seng", 4:"Kayu/Sirap", 5:"Asbes", 6:"Bambu/Jerami/Ijuk/Daun-daunan/Rumbia", 7:"Lainnya" },
            dinding_utama: { 1:"Tembok", 2:"Plesteran anyaman bambu/kawat", 3:"Kayu/papan/batang kayu", 4:"Bambu/Anyaman bambu", 5:"Lainnya" },
            lantai_utama: { 1:"Marmer/Granit", 2:"Keramik/Ubin/Tegel/Teraso", 3:"Parket/Vinil/Karpet", 4:"Kayu/Papan", 5:"Semen/Bata Merah", 6:"Bambu/Tanah", 7:"Lainnya" },
            fasilitas_bab: { 1:"Ada, digunakan keluarga sendiri", 2:"Ada, digunakan bersama keluarga tertentu", 3:"Ada, MCK komunal", 4:"Ada, MCK umum", 5:"Ada, keluarga tidak menggunakan", 6:"Tidak ada fasilitas" },
            jenis_kloset: { 1:"Leher angsa", 2:"Plengsengan dengan tutup", 3:"Plengsengan tanpa tutup", 4:"Cemplung/Cubluk" },
            pembuangan_akhir_tinja: { 1:"Tangki septik", 2:"IPAL", 3:"Kolam/Sawah/Sungai/Danau/Laut", 4:"Lubang tanah", 5:"Pantai/Tanah lapang/Kebun", 6:"Lainnya" },
            bahan_bakar_memasak: { 1:"Listrik", 2:"Elpiji 5,5 kg/blue gas", 3:"Elpiji 12 kg", 4:"Elpiji 3 kg", 5:"Gas kota", 6:"Biogas", 7:"Minyak tanah", 8:"Briket", 9:"Arang", 10:"Kayu bakar", 11:"Lainnya" },
            sumber_penerangan: { 1:"Listrik PLN dengan meteran", 2:"Listrik PLN tanpa meteran", 3:"Listrik Non PLN", 4:"Bukan listrik" },
            tempat_buang_sampah: { 1:"Pengangkutan sampah rutin", 2:"Lubang/dibakar", 3:"Sungai/irigasi/danau/laut", 4:"Drainase", 5:"Lainnya" },
            sumber_air_minum: { 1:"Air kemasan bermerek", 2:"Air isi ulang", 3:"Ledeng dengan meteran", 4:"Ledeng tanpa meteran", 5:"Sumur bor/pompa", 6:"Sumur", 7:"Mata air", 8:"Sungai/danau/kolam", 9:"Air hujan", 10:"Lainnya" },
            sumber_air_mandi_cuci: { 1:"Ledeng dengan meteran", 2:"Ledeng tanpa meteran", 3:"Sumur bor/pompa", 4:"Sumur", 5:"Mata air", 6:"Sungai/danau/kolam", 7:"Air hujan", 8:"Lainnya" },
            blt_desa: { 1:"Ya", 2:"Tidak" }, pkh: { 1:"Ya", 2:"Tidak" }, bpjs_pbi: { 1:"Ya", 2:"Tidak" },
            bantuan_pangan_pemerintah: { 1:"Ya", 2:"Tidak" }, bnpt_sembako: { 1:"Ya", 2:"Tidak" },
            pip: { 1:"Ya", 2:"Tidak" }, mbg: { 1:"Ya", 2:"Tidak" },
            pernah_terima_bansos_tidak_lagi_status: { 1:"Ada", 2:"Tidak ada" },
        };

        // ── COL_REMAP — variable names → dashboard column names ──
        const COL_REMAP = {
            'status_bangunan_tinggal': 'tempat_tinggal',
            'bukti_kepemilikan_tanah': 'bukti_kepemilikan',
            'atap_utama': 'jenis_atap',
            'dinding_utama': 'jenis_dinding',
            'lantai_utama': 'jenis_lantai',
            'pembuangan_akhir_tinja': 'pembuangan_tinja',
            'bahan_bakar_memasak': 'energi_memasak',
            'sumber_penerangan': 'penerangan_rumah',
            'sumber_air_mandi_cuci': 'sumber_air_mandi',
            'blt_desa': 'penerima_blt_desa',
            'pkh': 'penerima_pkh',
            'bpjs_pbi': 'penerima_bpjs_pbi',
            'bantuan_pangan_pemerintah': 'penerima_bantuan_pangan',
            'bnpt_sembako': 'penerima_bnpt_sembako',
            'pip': 'penerima_pip',
            'mbg': 'penerima_mbg',
            'pernah_terima_bansos_tidak_lagi_status': 'art_tidak_lagi_menerima',
            'no_hp_responden': 'no_hp',
            'jumlah_lansia_60plus': 'jumlah_lansia',
            'pekerja_migran_laki_laki': 'pekerja_migran_lk',
            'pekerja_migran_perempuan': 'pekerja_migran_pr',
        };

        // --- 2. DATA PROCESSING ---

        function decodeRow(row) {
            for (const [col, map] of Object.entries(KODE_LOOKUP)) {
                if (row[col] !== undefined && row[col] !== null && row[col] !== '') {
                    const code = Number(row[col]);
                    if (!isNaN(code) && map[code]) row[col] = map[code];
                }
            }
            return row;
        }

        function remapRow(row) {
            // Step 1: Map descriptive headers → variable names
            const varRow = {};
            for (const [key, val] of Object.entries(row)) {
                varRow[HEADER_TO_VAR[key] || key] = typeof val === 'string' ? val.trim() : val;
            }
            // Step 2: Decode codes → labels
            decodeRow(varRow);
            // Step 3: Remap to dashboard names
            const final = {};
            for (const [key, val] of Object.entries(varRow)) {
                final[COL_REMAP[key] || key] = val;
            }
            return final;
        }

        /**
         * Parse sheet dari template rapih.
         * Row layout: Row 1-3 = metadata, Row 4 = codes, Row 5 = headers, Row 6 = blank, Row 7+ = data
         * In 0-indexed aoa: [0-2] meta, [3] codes, [4] headers, [5] blank, [6+] data
         */
        function parseTemplateSheet(workbook, sheetName) {
            const ws = workbook.Sheets[sheetName];
            if (!ws) return [];
            const aoa = XLSX.utils.sheet_to_json(ws, { header: 1, defval: '' });
            if (aoa.length < 6) return [];
            const headers = aoa[4].map(h => String(h).trim());
            const data = [];
            for (let i = 6; i < aoa.length; i++) {
                const row = {};
                let hasData = false;
                for (let j = 0; j < headers.length; j++) {
                    if (headers[j]) {
                        row[headers[j]] = aoa[i][j] !== undefined ? aoa[i][j] : '';
                        if (aoa[i][j] !== '' && aoa[i][j] !== undefined && aoa[i][j] !== null) hasData = true;
                    }
                }
                if (hasData) data.push(row);
            }
            return data;
        }

        // --- 3. DATA LOADING ---

        async function loadData() {
            if (USE_LOCAL_XLSX) {
                try {
                    const response = await fetch(LOCAL_XLSX_PATH);
                    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    const arrayBuffer = await response.arrayBuffer();
                    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
                    console.log("Sheet tersedia:", workbook.SheetNames);

                    // Parse Entri_Keluarga
                    const rawKeluarga = parseTemplateSheet(workbook, 'Entri_Keluarga');
                    if (rawKeluarga.length > 0) {
                        dataKeluarga = rawKeluarga.map(remapRow);
                        console.log(`✓ Keluarga: ${dataKeluarga.length} baris`);
                        console.log("Sample:", dataKeluarga[0]);
                    } else {
                        console.warn("Sheet Entri_Keluarga kosong atau tidak ditemukan.");
                        alert("Sheet 'Entri_Keluarga' tidak ditemukan atau kosong.");
                        return;
                    }

                    // Parse supplementary sheets (optional — fail silently)
                    const rawLapangan = parseTemplateSheet(workbook, '403_Lapangan');
                    if (rawLapangan.length > 0) {
                        dataLapangan = rawLapangan;
                        console.log(`✓ 403_Lapangan: ${dataLapangan.length} baris`);
                    }

                    const rawAgama = parseTemplateSheet(workbook, '701_Agama');
                    if (rawAgama.length > 0) {
                        dataAgama = rawAgama;
                        console.log(`✓ 701_Agama: ${dataAgama.length} baris`);
                    }

                    const rawDisabilitas = parseTemplateSheet(workbook, '702_Disabilitas');
                    if (rawDisabilitas.length > 0) {
                        dataDisabilitas = rawDisabilitas;
                        console.log(`✓ 702_Disabilitas: ${dataDisabilitas.length} baris`);
                    }

                    const rawPendidikan = parseTemplateSheet(workbook, '601_Pendidikan_SLS');
                    if (rawPendidikan.length > 0) {
                        dataPendidikanSLS = rawPendidikan;
                        console.log(`✓ 601_Pendidikan: ${dataPendidikanSLS.length} baris`);
                    }

                    const rawKesehatan = parseTemplateSheet(workbook, '602_Kesehatan_SLS');
                    if (rawKesehatan.length > 0) {
                        dataKesehatanSLS = rawKesehatan;
                        console.log(`✓ 602_Kesehatan: ${dataKesehatanSLS.length} baris`);
                    }

                    // Parse Foto sheet (optional)
                    const rawFoto = parseTemplateSheet(workbook, 'Foto_Keluarga');
                    if (rawFoto.length > 0) {
                        rawFoto.forEach(r => {
                            const kk = String(r['Nomor KK'] || '').trim();
                            const fid = String(r['File ID Google Drive'] || '').trim();
                            if (kk && fid) dataFoto[kk] = fid;
                        });
                        console.log(`✓ Foto: ${Object.keys(dataFoto).length} entri`);
                    }

                } catch (error) {
                    console.error("Gagal memuat XLSX:", error);
                    alert("Gagal memuat file XLSX. Pastikan file tersedia dan jalankan via web server.\\nDetail: " + error.message);
                    return;
                }
            } else {
                // ── Google Sheets CSV mode ──
                if (!SPREADSHEET_ID) { alert("SPREADSHEET_ID belum diisi."); return; }
                try {
                    const loadCSV = (gid) => new Promise((resolve, reject) => {
                        if (!gid) { resolve({ data: [] }); return; }
                        const url = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/export?format=csv&gid=${gid}`;
                        Papa.parse(url, {
                            download: true, header: false, dynamicTyping: true, skipEmptyLines: true,
                            complete: res => {
                                // Template format: rows 0-3 = meta, row 4 = headers, row 5 = blank, row 6+ = data
                                const rows = res.data;
                                if (rows.length < 6) { resolve({ data: [] }); return; }
                                const headers = rows[4].map(h => String(h || '').trim());
                                const parsed = [];
                                for (let i = 6; i < rows.length; i++) {
                                    const obj = {};
                                    let hasData = false;
                                    for (let j = 0; j < headers.length; j++) {
                                        if (headers[j]) {
                                            obj[headers[j]] = rows[i][j] !== undefined ? rows[i][j] : '';
                                            if (rows[i][j] !== '' && rows[i][j] !== undefined && rows[i][j] !== null) hasData = true;
                                        }
                                    }
                                    if (hasData) parsed.push(obj);
                                }
                                resolve({ data: parsed });
                            },
                            error: reject
                        });
                    });

                    const resK = await loadCSV(SHEET_GIDS.keluarga);
                    if (resK.data.length > 0) {
                        dataKeluarga = resK.data.map(remapRow);
                    } else { alert("Data keluarga kosong."); return; }

                    const [resL, resA, resD, resP, resH] = await Promise.all([
                        loadCSV(SHEET_GIDS.lapangan), loadCSV(SHEET_GIDS.agama),
                        loadCSV(SHEET_GIDS.disabilitas), loadCSV(SHEET_GIDS.pendidikan),
                        loadCSV(SHEET_GIDS.kesehatan)
                    ]);
                    if (resL.data.length > 0) dataLapangan = resL.data;
                    if (resA.data.length > 0) dataAgama = resA.data;
                    if (resD.data.length > 0) dataDisabilitas = resD.data;
                    if (resP.data.length > 0) dataPendidikanSLS = resP.data;
                    if (resH.data.length > 0) dataKesehatanSLS = resH.data;

                    // Foto
                    const resF = await loadCSV(SHEET_GIDS.foto);
                    if (resF.data.length > 0) {
                        resF.data.forEach(r => {
                            const kk = String(r['Nomor KK'] || '').trim();
                            const fid = String(r['File ID Google Drive'] || '').trim();
                            if (kk && fid) dataFoto[kk] = fid;
                        });
                    }

                    console.log("Data berhasil dari Google Sheets!");
                } catch (error) {
                    console.error("Gagal dari Google Sheets:", error);
                    alert("Gagal terhubung ke Google Sheets.");
                    return;
                }
            }
            renderBerandaLokus();
            renderAll();
        }

        // --- 4. FILTERING ---
        let filterWilayah = 'Semua Lokus';

        function getFilteredKeluarga() {
            return dataKeluarga.filter(k => filterWilayah === 'Semua Lokus' || k.desa_kelurahan === filterWilayah);
        }

        // --- 5. HELPERS ---
        function formatNumber(num) { return num.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, "."); }
        function maskIdentifier(value, s = 4, e = 4) {
            const t = String(value || '');
            return t.length <= s + e ? '*'.repeat(t.length) : `${t.slice(0, s)}${'*'.repeat(t.length - s - e)}${t.slice(-e)}`;
        }
        function maskKK(v) { return maskIdentifier(v, 6, 4); }
        function countBy(arr, key) {
            const c = {};
            arr.forEach(r => { const v = String(r[key] || 'Lainnya').trim() || 'Lainnya'; c[v] = (c[v] || 0) + 1; });
            return c;
        }
        function sumField(arr, key) { return arr.reduce((s, r) => s + (Number(r[key]) || 0), 0); }

        const PALETTE = ['#8c5a3c','#5a7d6a','#c49a6c','#b85c4d','#a39080','#d4a27a','#6b6860','#7a9e7e','#c47a5c','#9b8a6e','#6e8b74','#c4946c'];

        function getChartOpts() {
            const isDark = document.documentElement.classList.contains('dark');
            const txtColor = isDark ? '#e8e5df' : '#1a1a18';
            return {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { labels: { color: txtColor, font: { family: "'Plus Jakarta Sans'" } } } }
            };
        }

        // --- 6. RENDER BERANDA & PROFIL ---

        function renderBerandaLokus() {
            const grid = document.getElementById('berandaLokusGrid');
            const profilContainer = document.getElementById('profilContentContainer');
            grid.innerHTML = '';
            profilContainer.innerHTML = '';

            lokusList.forEach((lokus, idx) => {
                const klg = dataKeluarga.filter(k => k.desa_kelurahan === lokus);
                const totalART = sumField(klg, 'jumlah_art');
                const totalLansia = sumField(klg, 'jumlah_lansia');
                const rmhMilik = klg.filter(k => k.tempat_tinggal === "Milik Sendiri").length;
                const bpjsPbi = klg.filter(k => k.penerima_bpjs_pbi === 'Ya').length;

                grid.innerHTML += `
                    <div class="lokus-card">
                        <h3><i data-lucide="${idx === 0 ? 'trees' : (idx === 1 ? 'waves' : 'building')}"></i> ${lokus}</h3>
                        <div class="lokus-stats-list">
                            <div><span>Jumlah Keluarga:</span> <strong>${klg.length}</strong></div>
                            <div><span>Total ART:</span> <strong>${totalART}</strong></div>
                            <div><span>Rata-rata ART:</span> <strong>${klg.length ? (totalART / klg.length).toFixed(1) : 0}</strong></div>
                            <div><span>Rumah Milik Sendiri:</span> <strong>${klg.length ? Math.round((rmhMilik / klg.length) * 100) : 0}%</strong></div>
                            <div><span>BPJS PBI:</span> <strong>${klg.length ? Math.round((bpjsPbi / klg.length) * 100) : 0}%</strong></div>
                        </div>
                        ${dataFoto[klg[0]?.nomor_kk] ? '<button class="btn btn-secondary" style="margin-top:0.75rem;width:100%" onclick="showPhoto(\\'' + klg[0].nomor_kk + '\\')"><i data-lucide="camera" style="width:16px;height:16px;"></i> Lihat Foto</button>' : ''}
                    </div>
                `;

                profilContainer.innerHTML += `
                    <div class="tab-content ${idx === 0 ? 'active' : ''}" id="profil-${lokus.toLowerCase().replace(/ /g, '-').replace('.', '')}">
                        <div style="background: var(--color-surface); padding: 2rem; border-radius: var(--radius-lg); border: 1px solid var(--color-border);">
                            <div class="badge-warning" style="display:inline-block; margin-bottom:1rem;">${klg[0]?.status_wilayah || (lokus.startsWith('Kelurahan') ? 'Kelurahan' : 'Desa')}</div>
                            <h3>${lokus}</h3>
                            <p class="text-muted" style="margin-bottom: 2rem;">Profil demografi dan kelayakan permukiman berdasarkan instrumen SDGs Desa Keluarga.</p>
                            <div class="kpi-grid">
                                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="home"></i> Keluarga</div><div class="kpi-value">${klg.length}</div></div>
                                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="users"></i> Total ART</div><div class="kpi-value">${totalART}</div></div>
                                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="heart-pulse"></i> Lansia (60+)</div><div class="kpi-value">${totalLansia}</div></div>
                            </div>
                        </div>
                    </div>
                `;
            });
            lucide.createIcons();
        }

        // --- 7. RENDER DASHBOARD KELUARGA ---
        let chartObjs = {};

        function destroyChart(key) {
            if (chartObjs[key]) { chartObjs[key].destroy(); chartObjs[key] = null; }
        }

        function makeChart(canvasId, type, labels, data, opts = {}) {
            const key = canvasId;
            destroyChart(key);
            const o = getChartOpts();
            chartObjs[key] = new Chart(document.getElementById(canvasId), {
                type,
                data: {
                    labels,
                    datasets: Array.isArray(data) && data[0]?.data
                        ? data
                        : [{ data, backgroundColor: PALETTE.slice(0, labels.length), borderWidth: 0, ...(opts.dsOpts || {}) }]
                },
                options: { ...o, ...opts }
            });
        }

        function renderDashboardKeluarga() {
            const klg = getFilteredKeluarga();
            const n = klg.length || 1;

            // KPI
            const bKlg = klg.filter(k => k.blt_desa === 'Ya' || k.pkh === 'Ya' || k.bpjs_pbi === 'Ya').length;
            const bsKlg = klg.filter(k => k.bantuan_pangan_pemerintah === 'Ya' || k.bnpt_sembako === 'Ya').length;
            const pKlg = klg.filter(k => k.pip === 'Ya' || k.mbg === 'Ya').length;
            const totalART = sumField(klg, 'jumlah_art');
            const milik = klg.filter(k => k.status_bangunan_tinggal === "Milik Sendiri").length;
            const listrikPLN = klg.filter(k => String(k.sumber_penerangan || '').includes("PLN")).length;
            const jamban = klg.filter(k => String(k.fasilitas_bab || '').includes("keluarga sendiri")).length;
            const pkh = klg.filter(k => k.pkh === 'Ya').length;
            const bpjsPbi = klg.filter(k => k.bpjs_pbi === 'Ya').length;

            document.getElementById('kpiKeluarga').innerHTML = `
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="home"></i> Total Keluarga</div><div class="kpi-value">${klg.length}</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="users"></i> Total ART</div><div class="kpi-value">${totalART}</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="calculator"></i> Rata-rata ART</div><div class="kpi-value">${klg.length ? (totalART / klg.length).toFixed(1) : 0}</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="key"></i> Milik Sendiri</div><div class="kpi-value">${Math.round((milik / n) * 100)}%</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="zap"></i> Listrik PLN</div><div class="kpi-value">${Math.round((listrikPLN / n) * 100)}%</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="droplets"></i> Jamban Sendiri</div><div class="kpi-value">${Math.round((jamban / n) * 100)}%</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="wallet"></i> PKH</div><div class="kpi-value">${Math.round((pkh / n) * 100)}%</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="shield-check"></i> BPJS PBI</div><div class="kpi-value">${Math.round((bpjsPbi / n) * 100)}%</div></div>
            `;

            // Charts
            const sTinggal = countBy(klg, 'status_bangunan_tinggal');
            makeChart('chartTinggal', 'doughnut', Object.keys(sTinggal), Object.values(sTinggal));

            // Bantuan
            const programs = [
                { key: 'blt_desa', label: 'BLT Desa' },
                { key: 'pkh', label: 'PKH' },
                { key: 'bpjs_pbi', label: 'BPJS PBI' },
                { key: 'bantuan_pangan_pemerintah', label: 'Bantuan Pangan' },
                { key: 'bnpt_sembako', label: 'BNPT/Sembako' },
                { key: 'pip', label: 'PIP' },
                { key: 'mbg', label: 'MBG' }
            ];
            destroyChart('chartBantuan');
            chartObjs['chartBantuan'] = new Chart(document.getElementById('chartBantuan'), {
                type: 'bar',
                data: { labels: programs.map(p => p.label), datasets: [{ label: 'Keluarga', data: programs.map(p => klg.filter(k => k[p.key] === 'Ya').length), backgroundColor: '#5a7d6a' }] },
                options: getChartOpts()
            });

            const sLantai = countBy(klg, 'jenis_lantai');
            makeChart('chartLantai', 'doughnut', Object.keys(sLantai), Object.values(sLantai));

            const sDinding = countBy(klg, 'jenis_dinding');
            makeChart('chartDinding', 'doughnut', Object.keys(sDinding), Object.values(sDinding));

            const sAtap = countBy(klg, 'jenis_atap');
            makeChart('chartAtap', 'doughnut', Object.keys(sAtap), Object.values(sAtap));

            const sPenerangan = countBy(klg, 'penerangan_rumah');
            makeChart('chartPenerangan', 'doughnut', Object.keys(sPenerangan), Object.values(sPenerangan));

            const sAir = countBy(klg, 'sumber_air_minum');
            makeChart('chartAirMinum', 'pie', Object.keys(sAir), Object.values(sAir));

            const sBab = countBy(klg, 'fasilitas_bab');
            makeChart('chartBAB', 'pie', Object.keys(sBab), Object.values(sBab));

            // Energi memasak
            const sEnergi = countBy(klg, 'energi_memasak');
            destroyChart('chartEnergi');
            chartObjs['chartEnergi'] = new Chart(document.getElementById('chartEnergi'), {
                type: 'bar',
                data: { labels: Object.keys(sEnergi), datasets: [{ label: 'Keluarga', data: Object.values(sEnergi), backgroundColor: PALETTE }] },
                options: getChartOpts()
            });

            const sSampah = countBy(klg, 'tempat_buang_sampah');
            makeChart('chartSampah', 'pie', Object.keys(sSampah), Object.values(sSampah));

            const sTinja = countBy(klg, 'pembuangan_tinja');
            makeChart('chartTinja', 'pie', Object.keys(sTinja), Object.values(sTinja));

            lucide.createIcons();
        }

        // --- 8. RENDER DASHBOARD SOSIAL ---

        function renderDashboardSosial() {
            const klg = getFilteredKeluarga();
            const n = klg.length || 1;

            // KPI
            const totalART = sumField(klg, 'jumlah_art');
            const totalLansia = sumField(klg, 'jumlah_lansia');
            const migranLk = sumField(klg, 'pekerja_migran_lk');
            const migranPr = sumField(klg, 'pekerja_migran_pr');
            const totalDisab = dataDisabilitas.reduce((s, r) => {
                const cols = Object.keys(r).filter(k => k !== 'ID keluarga sesuai Entri_Keluarga' && k !== 'Nomor KK' && k !== 'id_keluarga_ref' && k !== 'nomor_kk');
                return s + cols.reduce((ss, c) => ss + (Number(r[c]) || 0), 0);
            }, 0);

            document.getElementById('kpiSosial').innerHTML = `
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="users"></i> Total ART</div><div class="kpi-value">${totalART}</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="heart-pulse"></i> Lansia (60+)</div><div class="kpi-value">${totalLansia}</div><div class="kpi-sub">${totalART ? Math.round((totalLansia / totalART) * 100) : 0}% dari ART</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="plane"></i> Pekerja Migran</div><div class="kpi-value">${migranLk + migranPr}</div><div class="kpi-sub">L: ${migranLk}, P: ${migranPr}</div></div>
                <div class="kpi-card"><div class="kpi-card-header"><i data-lucide="accessibility"></i> Penyandang Disabilitas</div><div class="kpi-value">${totalDisab}</div></div>
            `;

            // Chart Lapangan Usaha (R403)
            if (dataLapangan.length > 0) {
                const sektorTotals = {};
                const skipCols = new Set(['ID keluarga sesuai Entri_Keluarga', 'Nomor KK', 'id_keluarga_ref', 'nomor_kk']);
                dataLapangan.forEach(row => {
                    for (const [key, val] of Object.entries(row)) {
                        if (skipCols.has(key)) continue;
                        const num = Number(val) || 0;
                        if (num > 0) sektorTotals[key] = (sektorTotals[key] || 0) + num;
                    }
                });
                const sorted = Object.entries(sektorTotals).sort((a, b) => b[1] - a[1]);
                destroyChart('chartLapanganUsaha');
                chartObjs['chartLapanganUsaha'] = new Chart(document.getElementById('chartLapanganUsaha'), {
                    type: 'bar',
                    data: { labels: sorted.map(e => e[0].length > 40 ? e[0].substring(0, 37) + '...' : e[0]), datasets: [{ label: 'Jumlah ART', data: sorted.map(e => e[1]), backgroundColor: '#5a7d6a' }] },
                    options: { ...getChartOpts(), indexAxis: 'y', plugins: { legend: { display: false }, tooltip: { callbacks: { title: ctx => { const idx = ctx[0].dataIndex; return sorted[idx][0]; } } } } }
                });
            }

            // Chart Agama (R701)
            if (dataAgama.length > 0) {
                const agamaCols = ['Jumlah Islam', 'Jumlah Kristen', 'Jumlah Katolik', 'Jumlah Buddha', 'Jumlah Hindu', 'Jumlah Konghucu', 'Jumlah Aliran penghayat kepercayaan'];
                const agamaLabels = ['Islam', 'Kristen', 'Katolik', 'Buddha', 'Hindu', 'Konghucu', 'Penghayat Kepercayaan'];
                const agamaTotals = agamaCols.map(col => dataAgama.reduce((s, r) => s + (Number(r[col]) || 0), 0));
                const filtered = agamaLabels.map((l, i) => [l, agamaTotals[i]]).filter(e => e[1] > 0);
                makeChart('chartAgama', 'pie', filtered.map(e => e[0]), filtered.map(e => e[1]));
            }

            // Chart Disabilitas (R702)
            if (dataDisabilitas.length > 0) {
                const disabCols = ['Tuna netra (buta)', 'Tuna rungu (tuli)', 'Tuna wicara (bisu)', 'Tuna rungu-wicara (tuli-bisu)', 'Tuna daksa/disabilitas tubuh', 'Tuna grahita/keterbelakangan mental', 'Tuna laras/eks-sakit jiwa', 'Eks-sakit kusta', 'Tuna ganda (fisik mental)'];
                const disabTotals = disabCols.map(col => dataDisabilitas.reduce((s, r) => s + (Number(r[col]) || 0), 0));
                const filteredDisab = disabCols.map((l, i) => [l, disabTotals[i]]).filter(e => e[1] > 0);
                if (filteredDisab.length > 0) {
                    destroyChart('chartDisabilitas');
                    chartObjs['chartDisabilitas'] = new Chart(document.getElementById('chartDisabilitas'), {
                        type: 'bar',
                        data: { labels: filteredDisab.map(e => e[0]), datasets: [{ label: 'Jumlah', data: filteredDisab.map(e => e[1]), backgroundColor: '#b85c4d' }] },
                        options: getChartOpts()
                    });
                }
            }

            // Table Pendidikan (R601)
            renderTablePendidikan();
            // Table Kesehatan (R602)
            renderTableKesehatan();

            lucide.createIcons();
        }

        function renderTablePendidikan() {
            const el = document.getElementById('tabelPendidikan');
            if (dataPendidikanSLS.length === 0) { el.innerHTML = '<p style="padding:1.5rem;color:var(--color-text-muted);">Data R601 belum tersedia.</p>'; return; }
            const facilities = ['Pos PAUD', 'TK/RA', 'SD/MI sederajat', 'SMP/MTs sederajat', 'SMA/MA sederajat', 'Perguruan Tinggi', 'Pesantren'];
            let html = '<table><thead><tr><th>SLS</th>';
            facilities.forEach(f => { html += `<th>${f}</th>`; });
            html += '</tr></thead><tbody>';
            dataPendidikanSLS.forEach(row => {
                const sls = row['SLS'] || row['Satuan Lingkungan Setempat (SLS)'] || '-';
                html += `<tr><td>${sls}</td>`;
                facilities.forEach(f => {
                    const negeri = row[`${f} - Negeri`];
                    const swasta = row[`${f} - Swasta`];
                    const jarak = row[`${f} - Jarak (Km)`];
                    const waktu = row[`${f} - Waktu (Menit)`];
                    const n = negeri == 1 ? '✓' : (negeri == 2 ? '✗' : '-');
                    const s = swasta == 1 ? '✓' : (swasta == 2 ? '✗' : '-');
                    const j = jarak || '-';
                    const w = waktu || '-';
                    html += `<td style="font-size:0.78rem;">N:${n} S:${s}<br>${j}km / ${w}m</td>`;
                });
                html += '</tr>';
            });
            html += '</tbody></table>';
            el.innerHTML = html;
        }

        function renderTableKesehatan() {
            const el = document.getElementById('tabelKesehatan');
            if (dataKesehatanSLS.length === 0) { el.innerHTML = '<p style="padding:1.5rem;color:var(--color-text-muted);">Data R602 belum tersedia.</p>'; return; }
            const facilities = ['Rumah sakit', 'Puskesmas dengan rawat inap', 'Puskesmas tanpa rawat inap', 'Puskesmas pembantu', 'Tempat praktik dokter', 'Tempat praktik bidan', 'Apotek'];
            let html = '<table><thead><tr><th>SLS</th>';
            facilities.forEach(f => { html += `<th>${f}</th>`; });
            html += '</tr></thead><tbody>';
            dataKesehatanSLS.forEach(row => {
                const sls = row['SLS'] || row['Satuan Lingkungan Setempat (SLS)'] || '-';
                html += `<tr><td>${sls}</td>`;
                facilities.forEach(f => {
                    const ada = row[`${f} - Keberadaan`];
                    const jarak = row[`${f} - Jarak (Km)`];
                    const waktu = row[`${f} - Waktu (Menit)`];
                    const status = ada == 1 ? '<span style="color:var(--color-success)">✓ Ada</span>' : (ada == 2 ? '<span style="color:var(--color-error)">✗</span>' : '-');
                    html += `<td style="font-size:0.78rem;">${status}<br>${jarak || '-'}km / ${waktu || '-'}m</td>`;
                });
                html += '</tr>';
            });
            html += '</tbody></table>';
            el.innerHTML = html;
        }

        // --- 9. RENDER ALL ---
        function renderAll() {
            renderDashboardKeluarga();
            renderDashboardSosial();
            renderBerandaLokus();
            if (typeof fetchVillagePopup === 'function') {
                fetchVillagePopup();
            }
        }

        // --- 10. EVENT LISTENERS ---
        // Theme Toggle
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
            themeIcon.setAttribute('data-lucide', 'sun');
        }
        themeToggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            themeIcon.setAttribute('data-lucide', document.documentElement.classList.contains('dark') ? 'sun' : 'moon');
            lucide.createIcons();
            renderAll();
        });

        // Tabs
        document.addEventListener('click', e => {
            if (e.target.classList.contains('tab-btn')) {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                e.target.classList.add('active');
                const target = document.getElementById(e.target.dataset.target);
                if (target) target.classList.add('active');
            }
        });

        // Mobile Menu
        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.getElementById('navLinks');
        menuToggle.addEventListener('click', () => navLinks.classList.toggle('active'));
        navLinks.addEventListener('click', () => { if (window.innerWidth <= 768) navLinks.classList.remove('active'); });

        // --- 11. PHOTO POPUP ---
        function showPhoto(kk) {
            const data = dataFoto[kk];
            if (!data || !data.file_id) return;
            const previewUrl = `https://drive.google.com/file/d/${data.file_id}/preview`;
            document.getElementById('photoPopupIframe').src = previewUrl;
            const driveLink = `https://drive.google.com/file/d/${data.file_id}/view`;
            const linkEl = document.getElementById('photoPopupLink');
            if (linkEl) linkEl.href = driveLink;
            document.getElementById('photoPopupOverlay').classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        window.showPhoto = showPhoto;

        function closePhotoPopup() {
            document.getElementById('photoPopupOverlay').classList.remove('active');
            document.body.style.overflow = '';
            document.getElementById('photoPopupIframe').src = '';
        }
        window.closePhotoPopup = closePhotoPopup;

        function fetchVillagePopup() {
            const popupUrl = `https://docs.google.com/spreadsheets/d/${POPUP_SPREADSHEET_ID}/export?format=csv`;
            const hardcodeId = '1gPDFURYAZTCWGWZxz5pPUwkdI5quy0G9';
            const hardcodeLink = 'https://drive.google.com/file/d/1gPDFURYAZTCWGWZxz5pPUwkdI5quy0G9/view?usp=sharing';

            function triggerPopup(fileId, driveLink) {
                setTimeout(() => {
                    document.getElementById('photoPopupIframe').src = `https://drive.google.com/file/d/${fileId}/preview`;
                    const linkEl = document.getElementById('photoPopupLink');
                    if (linkEl) linkEl.href = driveLink;
                    document.getElementById('photoPopupOverlay').classList.add('active');
                    document.body.style.overflow = 'hidden';
                }, 500); // deteksi otomatis
            }

            Papa.parse(popupUrl, {
                download: true,
                header: true,
                complete: function(results) {
                    if (results.data && results.data.length > 0) {
                        const villageDir = "''' + v['dir'].lower() + '''";
                        const row = results.data.find(r => r.nama && (r.nama.toLowerCase().includes(villageDir) || villageDir.includes(r.nama.toLowerCase())));
                        if (row && row.link) {
                            // Extract ID from link like https://drive.google.com/file/d/1gPDFURYAZTCWG.../view
                            const fileIdMatch = row.link.match(/\\/d\\/([a-zA-Z0-9_-]+)/);
                            const fileId = fileIdMatch ? fileIdMatch[1] : row.link;
                            triggerPopup(fileId, row.link);
                        } else {
                            triggerPopup(hardcodeId, hardcodeLink);
                        }
                    } else {
                        triggerPopup(hardcodeId, hardcodeLink);
                    }
                },
                error: function() {
                    triggerPopup(hardcodeId, hardcodeLink);
                }
            });
        }

        // --- 12. EXPORT ---
        window.exportAgregat = function (type) {
            const wb = XLSX.utils.book_new();
            const note = [['Data agregat Desa Cantik Buton Utara — Tanpa identitas personal (NIK/KK/Nama/Alamat/HP)'], []];

            if (type === 'keluarga' || type === 'gabungan') {
                const klg = getFilteredKeluarga();
                const head = ['No', 'Wilayah', 'Jumlah ART', 'Status Rumah', 'Jenis Atap', 'Jenis Dinding', 'Jenis Lantai', 'Energi Memasak', 'Penerangan', 'Air Minum', 'Fasilitas BAB', 'PKH', 'BPJS PBI', 'BLT Desa'];
                const rows = klg.map((k, i) => [
                    i + 1, k.desa_kelurahan, k.jumlah_art,
                    k.status_bangunan_tinggal, k.jenis_atap || '-', k.jenis_dinding || '-', k.jenis_lantai || '-',
                    k.energi_memasak || '-', k.sumber_penerangan || '-', k.sumber_air_minum || '-',
                    k.fasilitas_bab || '-', k.pkh || '-', k.bpjs_pbi || '-', k.blt_desa || '-'
                ]);
                const ws = XLSX.utils.aoa_to_sheet([...note, head, ...rows]);
                XLSX.utils.book_append_sheet(wb, ws, 'Tabel Keluarga');
            }
            if (type === 'sosial' || type === 'gabungan') {
                if (dataLapangan.length > 0) {
                    const skipCols = new Set(['ID keluarga sesuai Entri_Keluarga', 'Nomor KK']);
                    const sektorTotals = {};
                    dataLapangan.forEach(row => {
                        for (const [key, val] of Object.entries(row)) {
                            if (skipCols.has(key)) continue;
                            sektorTotals[key] = (sektorTotals[key] || 0) + (Number(val) || 0);
                        }
                    });
                    const head = ['No', 'Sektor', 'Jumlah ART'];
                    const rows = Object.entries(sektorTotals).sort((a, b) => b[1] - a[1]).map(([k, v], i) => [i + 1, k, v]);
                    const ws = XLSX.utils.aoa_to_sheet([...note, head, ...rows]);
                    XLSX.utils.book_append_sheet(wb, ws, 'Lapangan Usaha');
                }
                if (dataAgama.length > 0) {
                    const agamaCols = ['Jumlah Islam', 'Jumlah Kristen', 'Jumlah Katolik', 'Jumlah Buddha', 'Jumlah Hindu', 'Jumlah Konghucu'];
                    const head = ['No', 'Agama', 'Jumlah'];
                    const rows = agamaCols.map((c, i) => [i + 1, c.replace('Jumlah ', ''), dataAgama.reduce((s, r) => s + (Number(r[c]) || 0), 0)]);
                    const ws = XLSX.utils.aoa_to_sheet([...note, head, ...rows]);
                    XLSX.utils.book_append_sheet(wb, ws, 'Agama');
                }
            }
            XLSX.writeFile(wb, `Desa_Cantik_Agregat_${type.toUpperCase()}_2026.xlsx`);
        };

        // --- 13. AI INSIGHT ---
        let aiRawText = '';
        let aiChatHistory = [];
        let aiDataSummary = '';

        function aiGetApiUrl() { return 'https://buton-utara.net/api/ai-insight.php'; }

        function aiCollectDataSummary() {
            const klg = getFilteredKeluarga();
            const n = klg.length;
            const totalART = sumField(klg, 'jumlah_art');
            const totalLansia = sumField(klg, 'jumlah_lansia');
            const milik = klg.filter(k => k.tempat_tinggal === 'Milik Sendiri').length;
            const listrik = klg.filter(k => String(k.penerangan_rumah || '').includes('PLN')).length;
            const jamban = klg.filter(k => String(k.fasilitas_bab || '').includes('keluarga sendiri')).length;
            const pct = (v, t) => t ? `${Math.round((v / t) * 100)}%` : '0%';
            const cb = (key) => { const c = countBy(klg, key); return Object.entries(c).sort((a,b)=>b[1]-a[1]).map(([l,v])=>`${l}: ${v}`).join('; '); };

            const bantuan = [
                ['BLT Desa','penerima_blt_desa'],['PKH','penerima_pkh'],['BPJS PBI','penerima_bpjs_pbi'],
                ['Bantuan Pangan','penerima_bantuan_pangan'],['BNPT/Sembako','penerima_bnpt_sembako'],
                ['PIP','penerima_pip'],['MBG','penerima_mbg']
            ].map(([l,k])=>`${l}: ${klg.filter(r=>r[k]==='Ya').length}`).join('; ');

            let summary = [
                `Wilayah: ${lokusList.join(', ')}`,
                `Jumlah keluarga: ${n}`,
                `Total ART: ${totalART}`,
                `Rata-rata ART: ${n ? (totalART/n).toFixed(1) : 0}`,
                `Jumlah lansia (60+): ${totalLansia}`,
                '',
                'PERUMAHAN & LINGKUNGAN',
                `Rumah milik sendiri: ${milik} (${pct(milik, n)})`,
                `Listrik PLN: ${listrik} (${pct(listrik, n)})`,
                `Jamban keluarga sendiri: ${jamban} (${pct(jamban, n)})`,
                `Jenis atap: ${cb('jenis_atap')}`,
                `Jenis dinding: ${cb('jenis_dinding')}`,
                `Jenis lantai: ${cb('jenis_lantai')}`,
                `Sumber air minum: ${cb('sumber_air_minum')}`,
                `Fasilitas BAB: ${cb('fasilitas_bab')}`,
                `Energi memasak: ${cb('energi_memasak')}`,
                `Program bantuan: ${bantuan}`,
            ].join('\\n');

            if (dataLapangan.length > 0) {
                const skipCols = new Set(['ID keluarga sesuai Entri_Keluarga', 'Nomor KK']);
                const sektorTotals = {};
                dataLapangan.forEach(row => { for (const [key, val] of Object.entries(row)) { if (!skipCols.has(key)) sektorTotals[key] = (sektorTotals[key] || 0) + (Number(val) || 0); } });
                const top5 = Object.entries(sektorTotals).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([k,v])=>`${k}: ${v}`).join('; ');
                summary += '\\n\\nLAPANGAN USAHA (top 5)\\n' + top5;
            }
            if (dataAgama.length > 0) {
                const agamaCols = ['Jumlah Islam','Jumlah Kristen','Jumlah Katolik','Jumlah Buddha','Jumlah Hindu','Jumlah Konghucu'];
                const agamaData = agamaCols.map(c => `${c.replace('Jumlah ','')}: ${dataAgama.reduce((s,r)=>s+(Number(r[c])||0),0)}`).join('; ');
                summary += '\\n\\nAGAMA\\n' + agamaData;
            }
            return summary;
        }

        function aiMarkdownToHtml(text) {
            const escapeHtml = v => String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
            const inline = v => escapeHtml(v).replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
            const blocks = []; let list = [];
            const flushList = () => { if (!list.length) return; blocks.push(`<ul>${list.map(i=>`<li>${inline(i)}</li>`).join('')}</ul>`); list = []; };
            text.split(/\\r?\\n/).forEach(line => {
                const t = line.trim();
                if (!t) { flushList(); return; }
                if (t.startsWith('## ')) { flushList(); blocks.push(`<h2>${inline(t.slice(3))}</h2>`); return; }
                if (t.startsWith('- ')) { list.push(t.slice(2)); return; }
                flushList(); blocks.push(`<p>${inline(t)}</p>`);
            });
            flushList();
            return blocks.join('');
        }

        function aiAppendMessage(role, content, cls = '') {
            const list = document.getElementById('aiChatList');
            const msg = document.createElement('div');
            msg.className = `ai-message ${role} ${cls}`.trim();
            msg.innerHTML = role === 'assistant' ? aiMarkdownToHtml(content) : String(content).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
            list.appendChild(msg);
            document.getElementById('aiBody').scrollTop = document.getElementById('aiBody').scrollHeight;
        }

        function aiSetChatLoading(isLoading) {
            const input = document.getElementById('aiQuestion');
            const send = document.getElementById('aiSend');
            input.disabled = isLoading; send.disabled = isLoading;
            send.innerHTML = isLoading ? '<i data-lucide="loader-circle" style="width:18px;height:18px"></i>' : '<i data-lucide="send" style="width:18px;height:18px"></i>';
            lucide.createIcons();
        }

        function openAiInsight() {
            if (!dataKeluarga.length) { alert('Data belum dimuat.'); return; }
            const overlay = document.getElementById('aiOverlay');
            const body = document.getElementById('aiBody');
            const foot = document.getElementById('aiFoot');
            const fab = document.getElementById('aiFab');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            foot.style.display = 'none';
            fab.classList.add('loading');
            aiChatHistory = [];
            aiDataSummary = aiCollectDataSummary();
            body.innerHTML = '<div class="ai-chat-list" id="aiChatList"><div class="ai-skel">' + Array(8).fill('<div class="ai-skel-line"></div>').join('') + '</div></div>';

            fetch(aiGetApiUrl(), { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ context: aiDataSummary, mode: 'insight' }) })
            .then(r => r.json())
            .then(data => {
                fab.classList.remove('loading');
                body.innerHTML = '<div class="ai-chat-list" id="aiChatList"></div>';
                if (data.success) { aiRawText = data.analysis; aiAppendMessage('assistant', data.analysis); foot.style.display = 'flex'; document.getElementById('aiQuestion').focus(); }
                else { aiAppendMessage('assistant', data.error || 'Terjadi kesalahan.', 'error'); }
            })
            .catch(e => { fab.classList.remove('loading'); body.innerHTML = '<div class="ai-chat-list" id="aiChatList"></div>'; aiAppendMessage('assistant', 'Gagal terhubung ke server AI. ' + e.message, 'error'); });
        }

        function askAiQuestion(event) {
            event.preventDefault();
            const input = document.getElementById('aiQuestion');
            const q = input.value.trim();
            if (!q) return;
            if (q.length > 700) { aiAppendMessage('assistant', 'Pertanyaan terlalu panjang (max 700 karakter).', 'error'); return; }
            input.value = '';
            aiAppendMessage('user', q);
            aiChatHistory.push({ role: 'user', content: q });
            aiSetChatLoading(true);
            fetch(aiGetApiUrl(), { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ context: aiDataSummary || aiCollectDataSummary(), mode: 'chat', question: q, history: aiChatHistory.slice(-6) }) })
            .then(r => r.json())
            .then(data => {
                if (data.success) { aiRawText = data.analysis; aiAppendMessage('assistant', data.analysis); aiChatHistory.push({ role: 'assistant', content: data.analysis }); aiChatHistory = aiChatHistory.slice(-8); }
                else { aiAppendMessage('assistant', data.error || 'Terjadi kesalahan.', 'error'); }
            })
            .catch(e => { aiAppendMessage('assistant', 'Gagal terhubung: ' + e.message, 'error'); })
            .finally(() => { aiSetChatLoading(false); input.focus(); });
        }
        window.openAiInsight = openAiInsight;
        window.askAiQuestion = askAiQuestion;

        function closeAiModal() {
            document.getElementById('aiOverlay').classList.remove('active');
            document.body.style.overflow = '';
        }
        window.closeAiModal = closeAiModal;

        function copyAiResult() {
            navigator.clipboard.writeText(aiRawText).then(() => {
                const btn = document.querySelector('.ai-copy-btn');
                const orig = btn.innerHTML;
                btn.innerHTML = '<i data-lucide="check" style="width:14px;height:14px;"></i> Tersalin';
                btn.style.background = 'var(--color-success)'; btn.style.color = '#fff';
                lucide.createIcons();
                setTimeout(() => { btn.innerHTML = orig; btn.style.background = ''; btn.style.color = ''; lucide.createIcons(); }, 2000);
            });
        }
        window.copyAiResult = copyAiResult;

        // --- 14. INIT ---
        loadData();
        lucide.createIcons();
    </script>
</body>
</html>'''


# ─── 4. GENERATE FILES ───────────────────────────────────────────
for v in VILLAGES:
    full_html = head_section + '\n' + head_section.split('</head>')[0].endswith('</head>') * '' + get_body_html(v) + get_js(v)
    # Actually, just combine head + body + js
    full_html = head_section + '\n' + get_body_html(v) + get_js(v)

    filepath = os.path.join(v['dir'], 'index.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"[OK] Generated: {filepath} ({len(full_html)} bytes)")

print("\nSelesai! Semua 3 file berhasil di-generate.")
print("Untuk testing lokal, copy file Template_Data_Keluarga_Individu_rapih.xlsx ke folder desa sebagai 'data.xlsx'")
