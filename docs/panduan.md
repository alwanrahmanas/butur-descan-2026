# 📋 Panduan Koneksi Google Sheets → Website Desa Cantik

## Template yang Digunakan

File: [Template_Data_Keluarga_Individu.xlsx](file:///c:/Users/US3R/OneDrive/Dokumen/Kerja/2026/Desa Cantik/web/Template_Data_Keluarga_Individu.xlsx)

| Sheet | Kolom | Kolom yang Ditampilkan di Web | Kolom Sensitif (TIDAK ditampilkan) |
|-------|-------|------|------|
| **Keluarga** | 40 | `desa_kelurahan`, `tempat_tinggal`, `jenis_atap`, `energi_memasak`, `sumber_air_minum`, `penerima_pkh` | `nomor_kk`, `nik_kepala_keluarga`, `nama_responden`, `alamat`, `no_hp` |
| **Individu** | 15 | `desa_kelurahan`, `jenis_kelamin`, `umur`, `pendidikan_tertinggi`, `kondisi_pekerjaan`, `peserta_jaminan_kesehatan`, `peserta_jamsostek` | `nomor_kk`, `nik`, `nama` |

> [!IMPORTANT]
> Data sensitif tetap **diperlukan di spreadsheet** untuk relasi antar-tabel (via `nomor_kk`), tetapi **TIDAK pernah ditampilkan** di website maupun file Excel yang bisa diunduh publik.

---

## Langkah-Langkah Koneksi

### Langkah 1: Upload Template ke Google Drive

1. Buka [Google Drive](https://drive.google.com)
2. Klik **+ Baru** → **Upload file**
3. Pilih file `Template_Data_Keluarga_Individu.xlsx`
4. Setelah terupload, klik kanan → **Buka dengan** → **Google Spreadsheets**

### Langkah 2: Isi Data Lapangan

1. Isi data mulai **Baris ke-4** (baris 1-3 berisi disclaimer, blok referensi, dan nama kolom)
2. Sheet **Keluarga**: isi semua 40 kolom termasuk data sensitif
3. Sheet **Individu**: isi semua 15 kolom termasuk NIK dan nama
4. Pastikan `nomor_kk` di sheet Individu **sama persis** dengan di sheet Keluarga

### Langkah 3: Buka Akses Publik (Read-Only)

1. Klik tombol biru **"Bagikan" (Share)** di pojok kanan atas
2. Pada "Akses Umum", ubah dari **"Dibatasi"** → **"Siapa saja yang memiliki link"**
3. Pastikan perannya adalah **"Pelihat" (Viewer)** 
4. Klik **Selesai**

> [!WARNING]
> Jangan pilih "Editor"! Cukup "Viewer" agar orang lain tidak bisa mengubah data Anda.

### Langkah 4: Dapatkan ID Spreadsheet dan GID

Lihat URL di address bar browser Anda:

```
https://docs.google.com/spreadsheets/d/1AbCdEfGhIjKlMnOpQrStUvWxYz/edit#gid=0
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^         ^
                                       INI = SPREADSHEET_ID                    INI = GID
```

**Cara menemukan GID masing-masing sheet:**
- Klik tab **"Keluarga"** di bawah → lihat URL, catat angka setelah `gid=` (biasanya **0** untuk sheet pertama)
- Klik tab **"Individu"** di bawah → lihat URL, catat angka setelah `gid=` (misal: **1234567890**)

### Langkah 5: Masukkan ke Kode Website

Buka file `desa-cantik-buton-utara-keluarga.html`, cari bagian berikut (di awal blok `<script>`):

```javascript
// KONFIGURASI GOOGLE SHEETS
const SPREADSHEET_ID = ""; // ← Tempel Spreadsheet ID di sini
const GID_KELUARGA = "0"; // ← Tempel GID sheet Keluarga
const GID_INDIVIDU = ""; // ← Tempel GID sheet Individu
```

Contoh yang sudah diisi:

```javascript
const SPREADSHEET_ID = "1AbCdEfGhIjKlMnOpQrStUvWxYz";
const GID_KELUARGA = "0";
const GID_INDIVIDU = "1234567890";
```

### Langkah 6: Upload ke Hosting RumahWeb

1. Login ke **cPanel** RumahWeb Anda
2. Buka **File Manager** → masuk ke folder `public_html` (atau subdomain/subfolder yang diinginkan)
3. Upload file `desa-cantik-buton-utara-keluarga.html` yang sudah diedit
4. Akses website Anda di browser

---

## ✅ Selesai!

Sekarang setiap kali Anda mengubah data di Google Sheets:
- Pengunjung website akan **otomatis melihat data terbaru** saat refresh halaman
- Banner kuning di website akan berubah hijau bertuliskan **"DATA LIVE"**
- Data sensitif (NIK, KK, nama) **tidak pernah tampil** di website

## ⚠️ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Banner tetap kuning (dummy data) | Pastikan `SPREADSHEET_ID` sudah diisi dan akses sudah **"Siapa saja"** |
| Error "Gagal terhubung" | Pastikan spreadsheet sudah di-share sebagai **Viewer** publik |
| Data tidak update | Refresh browser (Ctrl+F5). Google Sheets CSV cache bisa delay 1-5 menit |
| GID salah | Klik tab sheet yang benar, periksa URL setelah `gid=` |
