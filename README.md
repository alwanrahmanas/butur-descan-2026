# Dashboard Statistik SDGs - Desa & Kelurahan Cantik (Buton Utara)

Repository ini berisi kode sumber untuk website landing page dan dashboard statistik SDGs Keluarga untuk program **Desa Cantik (Cinta Statistik)** di Kabupaten Buton Utara (Desa Laangke, Desa Malalanda, dan Kelurahan Lakonea).

---

## 📂 Struktur Repositori

```text
├── index.html                   # Landing Page utama Desa Cantik
├── Laangke/                     # Dashboard Desa Laangke
│   └── index.html
├── Lakonea/                     # Dashboard Kelurahan Lakonea
│   └── index.html
├── Malalanda/                   # Dashboard Desa Malalanda
│   └── index.html
├── api/                         # Backend API (PHP)
│   ├── data.php                 # Proxy Secure Google Sheets (Pencegah kebocoran ID)
│   ├── config.php               # Konfigurasi API & Cache
│   ├── ai-insight.php           # Fitur AI Analisis Data
│   └── .htaccess                # Aturan Keamanan & Environment variables
├── chatbot-n8n/                 # Workflow n8n Chatbot WhatsApp RAG
├── generate_dashboard.py        # Python Generator Script (Meng-update 3 HTML desa)
├── build_deploy.ps1             # Script PowerShell untuk mem-build deploy.zip
└── README.md
```

---

## 🔒 Fitur Baru: Arsitektur Secure Proxy Backend

Untuk menghindari kebocoran data sensitif (NIK/Nama) dan ID Google Spreadsheet ke publik melalui *View Page Source* atau *Network Inspector*, website ini menggunakan sistem **Secure Proxy Backend**:

1. **Proxy PHP (`api/data.php`):** Menarik data secara rahasia dari Google Sheets di sisi server (menggunakan cURL). Pengunjung tidak pernah melihat URL Google Sheets asli.
2. **Server Caching:** File hasil tarikan dari Google Sheets di-cache selama **5 menit** untuk meningkatkan performa loading halaman dan mengurangi latensi.
3. **Validasi Input:** Dilengkapi dengan pengecekan regex untuk menangkal celah keamanan (*cURL Injection*).

---

## 🚀 Panduan Deployment ke cPanel (Rumahweb)

1. Jalankan `build_deploy.ps1` di komputer lokal untuk menghasilkan file `deploy.zip`.
2. Upload file **`deploy.zip`** ke direktori `public_html` di cPanel File Manager Anda, lalu klik **Extract**.
3. Buka file **`api/.htaccess`** di cPanel Anda, lalu tambahkan baris *Environment Variable* berikut di baris paling bawah untuk menyimpan ID Google Sheets:
   ```apache
   SetEnv SHEET_ID_LAANGKE "ID_SPREADSHEET_LAANGKE"
   SetEnv SHEET_ID_LAKONEA "ID_SPREADSHEET_LAKONEA"
   SetEnv SHEET_ID_MALALANDA "ID_SPREADSHEET_MALALANDA"
   SetEnv SHEET_ID_POPUP "ID_SPREADSHEET_POPUP_FOTO"
   ```
4. Pastikan folder `api` memiliki hak akses (*Permissions*) **`0755`** dan file `data.php` memiliki hak akses **`0644`**.

---

## 🤖 Chatbot WhatsApp RAG (n8n & WAHA)

Folder `chatbot-n8n/` berisi berkas ekspor JSON alur kerja (*workflow*) n8n untuk bot asisten WhatsApp pintar berbasis RAG:
* Memiliki parser intent cerdas untuk menjawab teori/kuesioner pendataan.
* Menggunakan reranker hybrid berbasis JavaScript untuk mencari dokumen pendataan yang paling relevan.
* Terintegrasi dengan WhatsApp HTTP API (WAHA).

---

## 🛠️ Pengembangan Lokal

Jika Anda mengubah template HTML atau menambahkan fitur di masa depan, lakukan perubahan di dalam script **`generate_dashboard.py`** dan file CSS **`Laangke/index.html`** (sebagai basis CSS utama), kemudian jalankan:
```bash
python generate_dashboard.py
```
Script tersebut akan menyelaraskan dan memperbarui ketiga file HTML desa secara otomatis.
