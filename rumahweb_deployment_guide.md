# Panduan Deployment Desa Cantik ke Rumahweb (cPanel & Subdomain)

Dokumen ini berisi panduan langkah demi langkah untuk men-deploy aplikasi web **Desa Cantik** ke hosting **Rumahweb** menggunakan **cPanel**, termasuk konfigurasi subdomain untuk masing-masing lokus desa.

> **Referensi Panduan Resmi Rumahweb:**
> - [Pengertian dan Cara Membuat Subdomain](https://www.rumahweb.com/journal/subdomain-adalah/)
> - [Cara Upload Web ke Hosting cPanel Melalui File Manager](https://www.rumahweb.com/journal/cara-upload-web-ke-hosting-cpanel/)

---

## 📋 Ikhtisar Arsitektur Server & Konsep Subdomain

Berdasarkan panduan Rumahweb, **subdomain** adalah bagian dari sebuah nama domain induk. Subdomain umumnya digunakan sebagai pembagian area dari sebuah website, atau untuk membuat website baru yang berbeda kontennya dengan website utama, tanpa harus membeli domain baru.

Desain deployment ini menggunakan satu domain utama untuk API terpusat, sementara halaman web masing-masing desa disajikan melalui subdomain terpisah:

*   **Domain Utama (API)**: `https://buton-utara.net/api/ai-insight.php`
*   **Subdomain Desa**:
    *   `https://laangke.buton-utara.net` (diarahkan ke folder `public_html/Laangke`)
    *   `https://lakonea.buton-utara.net` (diarahkan ke folder `public_html/Lakonea`)
    *   `https://malalanda.buton-utara.net` (diarahkan ke folder `public_html/Malalanda`)

Dengan konfigurasi ini, file `.html` masing-masing desa akan memanggil API OpenAI terpusat di domain utama menggunakan mekanisme **CORS** yang sudah dikonfigurasi secara aman di `api/config.php`.

---

## 🚀 Langkah 1: Persiapan File ZIP (Lokal)

Pertama, buat paket ZIP bersih yang hanya berisi file *production* (tanpa file *development* seperti skrip Python atau template Excel):

1.  Buka terminal PowerShell di VS Code pada direktori root proyek (`web/`).
2.  Jalankan skrip auto-zip yang sudah disediakan:
    ```powershell
    .\build_deploy.ps1
    ```
3.  Proses ini akan menghasilkan file **`deploy.zip`** di direktori proyek Anda.

---

## 🌐 Langkah 2: Konfigurasi Subdomain di cPanel

Sebelum mengunggah file, Anda perlu membuat subdomain untuk masing-masing desa di cPanel. Sesuai panduan Rumahweb, berikut langkah-langkahnya:

1.  Login ke **cPanel Rumahweb** Anda.
2.  Cari dan pilih menu **Domains** (atau **Subdomains** pada tema cPanel klasik).
3.  Klik **Create A New Domain** (atau **Add Subdomain**).
4.  Tambahkan ketiga subdomain berikut secara bergiliran:

    ### Subdomain 1: Laangke
    *   **Domain (Subdomain)**: `laangke.buton-utara.net`
    *   **Document Root**: `public_html/Laangke` (pastikan diarahkan ke folder desa ini di dalam `public_html`)

    ### Subdomain 2: Lakonea
    *   **Domain (Subdomain)**: `lakonea.buton-utara.net`
    *   **Document Root**: `public_html/Lakonea`

    ### Subdomain 3: Malalanda
    *   **Domain (Subdomain)**: `malalanda.buton-utara.net`
    *   **Document Root**: `public_html/Malalanda`

5.  Klik **Submit** untuk membuat subdomain tersebut.

---

## 📤 Langkah 3: Mengunggah & Mengekstrak File Melalui File Manager

Setelah subdomain dibuat, langkah selanjutnya adalah mengunggah dan mengekstrak file web Anda melalui fitur File Manager cPanel, sebagaimana direkomendasikan oleh tutorial Rumahweb:

1.  Di halaman utama cPanel, cari bagian *Files* lalu buka menu **File Manager**.
2.  Masuk ke direktori utama website Anda, yaitu folder **`public_html`**.
3.  Klik tombol **Upload** di menu bagian atas, pilih file **`deploy.zip`** dari komputer lokal Anda.
4.  Tunggu hingga proses upload selesai (bar berwarna hijau mencapai 100%), lalu kembali ke jendela File Manager.
5.  Klik kanan pada file `deploy.zip`, pilih **Extract**, lalu pastikan direktori ekstraksi diarahkan ke **`/public_html`**. Klik *Extract File(s)*.
6.  Setelah berhasil diekstrak, Anda akan melihat struktur folder seperti ini di dalam `public_html`:
    *   `api/`
    *   `assets/`
    *   `Laangke/` (subdomain `laangke.` akan otomatis membaca folder ini sesuai *Document Root* yang diset pada Langkah 2)
    *   `Lakonea/` (subdomain `lakonea.` akan otomatis membaca folder ini)
    *   `Malalanda/` (subdomain `malalanda.` akan otomatis membaca folder ini)
    *   `desa-cantik-buton-utara.html`
    *   `desa-cantik-buton-utara-keluarga.html`
7.  (Opsional) Anda dapat menghapus file `deploy.zip` dari server untuk menghemat kapasitas disk (storage) hosting.

---

## 🔑 Langkah 4: Konfigurasi API Key OpenAI di Hosting

Agar fitur AI Insight dapat terhubung dengan OpenAI, Anda harus memasukkan API Key di file konfigurasi server:

1.  Di File Manager cPanel, masuk ke folder **`public_html/api`**.
2.  Cari file bernama **`.htaccess`**, klik kanan, lalu pilih **Edit**.
    > *Catatan: Jika file tidak terlihat, klik tombol **Settings** di pojok kanan atas File Manager cPanel, centang opsi **"Show Hidden Files (dotfiles)"**, lalu klik Save.*
3.  Temukan baris ke-16:
    ```apache
    # SetEnv OPENAI_API_KEY "sk-your-key-here"
    ```
4.  Hilangkan tanda pagar (`#`) di depannya dan ganti `"sk-your-key-here"` dengan API Key OpenAI Anda yang asli:
    ```apache
    SetEnv OPENAI_API_KEY "sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```
5.  Klik **Save Changes** di pojok kanan atas editor cPanel.

---

## 🏠 Langkah 5: Mengonfigurasi Halaman Utama Domain Utama

Agar saat seseorang mengunjungi domain utama `https://buton-utara.net` langsung diarahkan ke halaman dashboard utama (bukan tampilan kosong/direktori):

1.  Di File Manager cPanel, masuk ke folder **`public_html`**.
2.  Cari file **`desa-cantik-buton-utara.html`**.
3.  Klik kanan pada file tersebut, pilih **Rename**.
4.  Ganti namanya menjadi **`index.html`**.

Dengan begini, web server akan mengenali file tersebut sebagai halaman utama (landing page) dari domain utama Anda.

---

## 🔒 Langkah 6: Validasi SSL (PENTING)

Fitur API Insight memerlukan enkripsi HTTPS agar berjalan dengan lancar dan aman.
1.  Di cPanel, cari menu **SSL/TLS Status**.
2.  Pastikan semua domain (`buton-utara.net`, `www.buton-utara.net`) dan semua subdomain (`laangke.`, `lakonea.`, `malalanda.`) memiliki status SSL aktif (ikon gembok berwarna hijau).
3.  Jika belum aktif, klik tombol **Run AutoSSL** dan tunggu beberapa menit hingga proses сертификаasi otomatis selesai.

---

## ⚡ Pengujian Akhir
Setelah semua langkah selesai dilakukan, silakan lakukan uji coba:
1.  Buka `https://laangke.buton-utara.net` di browser Anda.
2.  Coba gunakan fitur chat AI atau klik tombol analisis AI.
3.  Respons harus keluar dengan benar, menandakan frontend di subdomain berhasil menghubungi API backend di domain utama secara aman dan terjaga.
