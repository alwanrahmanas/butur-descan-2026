# Plan Web Desa Cantik (Cinta Statistik) — Versi Unit Observasi Keluarga
## Dokumen Brief Super Detail untuk AI Website Builder Agent

***

## 1. Ringkasan Proyek

**Nama proyek:** Website Desa Cantik (Cinta Statistik) Kabupaten Buton Utara  
**Lokus:** Desa Malalanda, Desa Laangke, Kelurahan Lakonea  
**Status:** Prototype web  
**Status data:** Dummy data (simulasi), tetapi struktur variabel, tipe data, karakteristik field, dan logika relasi harus mengikuti kuesioner terbaru  
**Hosting target:** Rumahweb shared hosting / web hosting biasa  

### Perubahan penting dari brief sebelumnya
Unit observasi **bukan lagi RT**, melainkan **keluarga/rumah tangga** berdasarkan dokumen terbaru “SDGs Desa Kuesioner Rumah Tangga”, dan ada pula data turunan level **individu** berdasarkan bagian “SDGs Desa Kuesioner Individu”. Maka arsitektur data website harus diubah dari model “1 RT = 1 observasi” menjadi model **“1 keluarga/rumah tangga = 1 observasi utama”**, dengan data individu sebagai entitas anak yang terhubung melalui Nomor KK dan NIK.[1]

Artinya, website prototype harus menampilkan statistik berbasis keluarga/rumah tangga, misalnya kondisi permukiman, akses layanan dasar, penerima program pemerintah, pendidikan anggota keluarga, pekerjaan, kesehatan, dan karakteristik sosial lainnya.[1]

***

## 2. Tujuan Website

Website ini harus berfungsi sebagai:

1. **Media publikasi statistik keluarga/rumah tangga** untuk tiga lokus program Desa Cantik.
2. **Dashboard prototype** yang menunjukkan bagaimana data keluarga dan individu akan ditampilkan setelah pendataan riil selesai.
3. **Sarana komunikasi ke atasan/stakeholder** bahwa sistem digital Desa Cantik sudah dirancang dengan struktur yang sesuai instrumen terbaru.
4. **Sarana unduh data simulasi** dalam format Excel.
5. **Fondasi sistem final**, sehingga nanti ketika data lapangan masuk, yang diganti hanya valuenya, bukan struktur websitenya.[1]

***

## 3. Prinsip Arsitektur Data

### 3.1 Unit observasi utama
Unit observasi utama adalah **keluarga/rumah tangga**. Hal ini terlihat dari bagian awal kuesioner terbaru yang memuat “SDGs Desa Kuesioner Rumah Tangga”, dengan identitas seperti nomor KK, NIK kepala keluarga, deskripsi lokasi, dan karakteristik permukiman rumah tangga.[1]

### 3.2 Entitas turunan
Selain rumah tangga, dokumen juga memuat **kuesioner individu** yang berisi identitas individu, pekerjaan, penghasilan, kesehatan, disabilitas, pendidikan, bahasa, dan partisipasi sosial. Karena itu, sistem web harus dirancang minimal dengan dua entitas data:  
- **Tabel/data keluarga** sebagai tabel utama.  
- **Tabel/data individu** sebagai tabel turunan yang terhubung ke keluarga melalui nomor KK.[1]

### 3.3 Implikasi untuk website
Dashboard publik tidak perlu menampilkan semua data individu satu per satu, tetapi harus mampu menghasilkan agregasi dari level individu, misalnya proporsi jenis kelamin, pendidikan tertinggi, peserta jaminan sosial, kondisi pekerjaan, atau penyakit tertentu.[1]

***

## 4. Model Data yang Harus Dipakai

AI agent wajib membangun website dengan pendekatan berikut:

- **Data utama:** `dataKeluarga`
- **Data turunan:** `dataIndividu`
- **Relasi utama:** `nomor_kk`
- **Relasi tambahan:** `nik` untuk individu dan `nik_kepala_keluarga` untuk keluarga
- **Agregasi wilayah:** berdasarkan `desa_kelurahan`
- **Lokus:** Malalanda, Laangke, Lakonea

### 4.1 Dataset utama: keluarga
Setiap baris dalam `dataKeluarga` mewakili **1 keluarga/rumah tangga**.[1]

### 4.2 Dataset turunan: individu
Setiap baris dalam `dataIndividu` mewakili **1 individu/anggota keluarga** dan harus memiliki `nomor_kk` agar bisa digabung atau difilter berdasarkan keluarga asalnya.[1]

***

## 5. Struktur Variabel Keluarga

Struktur berikut harus mengikuti isi kuesioner rumah tangga terbaru. Field boleh disederhanakan untuk kebutuhan prototype, tetapi **nama logika variabel dan karakternya harus tetap setia** pada instrumen.[1]

### 5.1 Identitas keluarga
Ambil dari bagian P2 dan P3 rumah tangga.[1]

```javascript
const dataKeluarga = [
  {
    id_keluarga: "KLG-MLL-001",
    desa_kelurahan: "Desa Malalanda",
    status_wilayah: "Desa",
    kecamatan: "Kulisusu",
    kabupaten_kota: "Buton Utara",
    provinsi: "Sulawesi Tenggara",
    rw: "001",
    rt: "001",
    nama_responden: "Wa Ode Sari",
    alamat: "Jl. Contoh 1",
    no_hp: "0812xxxxxxx",
    no_telepon_rumah: "",
    nomor_kk: "7408XXXXXXXXXXXX",
    nik_kepala_keluarga: "7408XXXXXXXXXXXX",
    tahun_data: 2025,
```

### 5.2 Permukiman dan kondisi rumah
Bagian ini berasal dari blok P4 rumah tangga, yang mencakup tempat tinggal, status lahan, luas lantai/lahan, jenis lantai, dinding, jendela, atap, penerangan, energi memasak, sampah, MCK, air mandi, jamban, air minum, limbah cair, lokasi risiko, dan kekumuhan.[1]

```javascript
    tempat_tinggal: "Milik sendiri",             // Milik sendiri | Kontrak/Sewa | Bebas sewa | Dipinjami | Dinas | Lainnya
    status_lahan: "Milik sendiri",              // Milik sendiri | Milik orang lain | Tanah negara | Lainnya
    luas_lantai_m2: 72,
    luas_lahan_m2: 140,
    jenis_lantai: "Keramik",
    jenis_dinding: "Semen/beton/kayu berkualitas tinggi",
    kondisi_jendela: "Ada, berfungsi",
    jenis_atap: "Genteng",
    penerangan_rumah: "Listrik PLN",
    energi_memasak: "Gas/LPG/Biogas",
    sumber_kayu_bakar: "",                      // Isi bila energi_memasak = kayu bakar
    tempat_pembuangan_sampah: "Tempat sampah diangkut reguler",
    fasilitas_mck: "Sendiri",
    sumber_air_mandi: "Mata air/sumur/perpipaan",
    fasilitas_bab: "Jamban sendiri",
    sumber_air_minum: "Ledeng/perpipaan berbayar/air isi ulang/kemasan",
    pembuangan_limbah_cair: "Tangki/instalasi pengelolaan limbah",
    rumah_di_bawah_sutet: false,
    rumah_di_bantaran_sungai: false,
    rumah_di_lereng: false,
    kondisi_rumah: "Tidak kumuh",
```

### 5.3 Akses layanan dasar
Kuesioner memuat akses pendidikan terdekat, fasilitas kesehatan terdekat, tenaga kesehatan terdekat, dan akses transportasi ke tujuan penting seperti pekerjaan, lahan, sekolah, berobat, ibadah, dan rekreasi.[1]

Untuk prototype, simpan dalam bentuk variabel ringkas/agregat agar website mudah dibangun namun tetap setia pada instrumen.

```javascript
    jarak_paud_km: 0.8,
    jarak_sd_km: 1.2,
    jarak_smp_km: 4.5,
    jarak_sma_km: 8.0,
    akses_pendidikan_mudah: true,

    jarak_puskesmas_km: 3.5,
    jarak_posyandu_km: 0.6,
    akses_kesehatan_mudah: true,

    jarak_dokter_umum_km: 5.5,
    jarak_bidan_km: 1.0,
    akses_tenaga_kesehatan_mudah: true,

    moda_ke_pekerjaan: "Darat",
    transportasi_umum_ke_pekerjaan: true,
    waktu_tempuh_pekerjaan_jam: 0.4,
    biaya_transport_pekerjaan: 10000,
    akses_transportasi_mudah: true,
```

### 5.4 Program pemerintah
Kuesioner keluarga menanyakan penerimaan berbagai program pemerintah seperti BLT Dana Desa, PKH, BST, Banpres, Bantuan UMKM, bantuan pekerja, dan bantuan pendidikan anak.[1]

```javascript
    penerima_blt_desa: false,
    penerima_pkh: true,
    penerima_bst: false,
    penerima_banpres: false,
    penerima_bantuan_umkm: false,
    penerima_bantuan_pekerja: false,
    penerima_bantuan_pendidikan_anak: true,
    penerima_bantuan_lainnya: false
  }
];
```

***

## 6. Struktur Variabel Individu

Bagian kuesioner individu memuat identitas personal, pekerjaan, jaminan sosial ketenagakerjaan, sumber penghasilan setahun terakhir, penyakit, kunjungan fasilitas kesehatan, jaminan sosial kesehatan, disabilitas, pendidikan tertinggi, bahasa, dan partisipasi sosial.[1]

Untuk prototype, AI agent harus membuat dataset `dataIndividu` yang terhubung ke `dataKeluarga` melalui `nomor_kk`.[1]

```javascript
const dataIndividu = [
  {
    id_individu: "IND-MLL-001-01",
    nomor_kk: "7408XXXXXXXXXXXX",
    nik: "7408YYYYYYYYYYYY",
    nama: "Wa Ode Sari",
    jenis_kelamin: "Perempuan",
    tempat_lahir: "Buton Utara",
    tanggal_lahir: "1990-05-17",
    status_pernikahan: "Kawin",
    agama: "Islam",
    suku_bangsa: "Buton",
    kewarganegaraan: "WNI",
    no_hp: "0812xxxxxxx",
    whatsapp: "0812xxxxxxx",
    email: "",
    facebook: "",
    twitter: "",
    instagram: "",

    kondisi_pekerjaan: "Ibu rumah tangga",     // bersekolah | ibu rumah tangga | tidak bekerja | mencari pekerjaan | bekerja
    pekerjaan_utama: "Lainnya",
    peserta_jamsostek: false,
    penghasilan_setahun_rp: 0,
    sumber_penghasilan_utama: "Sumbangan dari keluarga/pemerintah",

    sakit_diare: false,
    sakit_dbd: false,
    sakit_malaria: false,
    sakit_covid19: false,
    sakit_jantung: false,
    sakit_tbc: false,
    sakit_diabetes: false,
    punya_disabilitas: false,
    peserta_jaminan_kesehatan: true,
    kunjungan_puskesmas_setahun: 1,
    kunjungan_posyandu_setahun: 0,
    kunjungan_bidan_setahun: 1,

    pendidikan_tertinggi: "SMA dan sederajat",
    bahasa_rumah: "Bahasa Wolio",
    bahasa_formal: "Bahasa Indonesia",
    kerja_bakti_setahun: 3,
    siskamling_setahun: 0,
    pesta_rakyat_setahun: 1,
    menolong_warga_meninggal_setahun: 2,
    menolong_warga_sakit_setahun: 3,
    menolong_warga_kecelakaan_setahun: 0
  }
];
```

***

## 7. Volume Dummy Data yang Harus Dibuat

Untuk prototype, gunakan volume dummy data yang cukup untuk membuat dashboard terasa nyata namun tetap ringan di browser.[1]

### 7.1 Dataset keluarga
Buat **30 keluarga dummy** dengan distribusi:
- 10 keluarga — Desa Malalanda
- 10 keluarga — Desa Laangke
- 10 keluarga — Kelurahan Lakonea

### 7.2 Dataset individu
Buat **120 individu dummy** dengan asumsi rata-rata 4 anggota per keluarga.[1]

### 7.3 Pola karakteristik antar wilayah
Agar dashboard komparatif terlihat masuk akal, bentuk pola dummy seperti ini:

- **Desa Malalanda:** lebih dominan rumah milik sendiri, akses pendidikan dan kesehatan sedang, sebagian rumah memakai kayu bakar, karakter lebih rural.
- **Desa Laangke:** variasi kondisi permukiman lebih beragam, beberapa rumah punya akses layanan lebih jauh, ada lebih banyak keluarga penerima program bantuan.
- **Kelurahan Lakonea:** lebih urban/peri-urban, akses layanan lebih dekat, listrik PLN dan air minum layak lebih dominan, proporsi pendidikan lebih tinggi.[1]

***

## 8. Fokus Konten Website

Karena unit observasi sekarang keluarga, website **tidak lagi berpusat pada RT** sebagai subjek utama dashboard. RT tetap boleh muncul sebagai identitas alamat, tetapi cerita data utama harus bergeser ke:

- kondisi rumah tangga,
- akses layanan dasar,
- penerima bantuan,
- komposisi anggota keluarga,
- kondisi pekerjaan dan pendidikan,
- kesehatan dan perlindungan sosial.[1]

***

## 9. Sitemap Website Baru

Website tetap dibuat sebagai **single-file HTML** dengan section-section berikut:

```
#beranda
#profil
#dashboard-keluarga
#dashboard-individu
#unduh-data
#tentang-data
#kontak
```

### Penjelasan section
- **Beranda:** pengantar program + ringkasan 3 lokus
- **Profil:** profil singkat Malalanda, Laangke, Lakonea
- **Dashboard Keluarga:** statistik level rumah tangga/keluarga
- **Dashboard Individu:** statistik level individu agregat
- **Unduh Data:** ekspor Excel keluarga, individu, dan gabungan
- **Tentang Data:** menjelaskan metode, dummy data, dan unit observasi
- **Kontak:** kontak BPS / pengelola

***

## 10. Beranda

### Komponen wajib
1. **Header sticky** dengan logo SVG “DC”, nama program, menu, tombol dark mode.
2. **Hero statement:**
   - Judul: `Desa Cantik Buton Utara`
   - Subjudul: `Prototype dashboard statistik keluarga dan individu untuk Desa Malalanda, Desa Laangke, dan Kelurahan Lakonea`
3. **Banner disclaimer:** `Data yang ditampilkan adalah data simulasi untuk prototype, belum merupakan hasil pendataan lapangan resmi.`
4. **Tiga kartu lokus** yang menampilkan:
   - jumlah keluarga,
   - jumlah individu,
   - rata-rata anggota keluarga,
   - persentase rumah tidak kumuh,
   - persentase peserta jaminan kesehatan.[1]

***

## 11. Dashboard Keluarga

Dashboard keluarga harus menampilkan indikator yang benar-benar relevan dengan kuesioner rumah tangga terbaru.[1]

### 11.1 Filter
Sediakan filter berikut:
- Dropdown wilayah: Semua Lokus / Malalanda / Laangke / Lakonea
- Filter status wilayah: Semua / Desa / Kelurahan
- Pencarian cepat berdasarkan nomor KK atau nama responden

### 11.2 KPI utama keluarga
Tampilkan kartu KPI berikut:
1. Total keluarga
2. Total anggota keluarga (hasil relasi dengan data individu)
3. Rata-rata anggota per keluarga
4. % rumah milik sendiri
5. % rumah tidak kumuh
6. % keluarga dengan listrik PLN
7. % keluarga dengan jamban sendiri
8. % keluarga dengan sumber air minum layak
9. % keluarga penerima PKH
10. % keluarga dengan akses kesehatan mudah.[1]

### 11.3 Grafik keluarga
Gunakan Chart.js dan tampilkan minimal:

**Chart A — Doughnut**
- Distribusi status tempat tinggal: milik sendiri / kontrak-sewa / bebas sewa / lainnya.[1]

**Chart B — Bar**
- Persentase rumah tidak kumuh per lokus.[1]

**Chart C — Stacked bar**
- Sumber energi memasak per lokus: gas/LPG/biogas, minyak tanah/batu bara, kayu bakar, lainnya.[1]

**Chart D — Horizontal bar**
- Penerima program pemerintah (BLT Desa, PKH, BST, Banpres, bantuan UMKM, bantuan pekerja, bantuan pendidikan anak) dihitung pada level keluarga.[1]

### 11.4 Tabel keluarga
Tampilkan tabel interaktif dengan kolom berikut:
- Nomor KK
- Desa/Kelurahan
- RT/RW
- Nama Responden
- Status rumah
- Kondisi rumah
- Listrik
- Air minum
- Jamban
- Penerima PKH
- Jumlah anggota keluarga

Setiap baris harus bisa di-expand untuk menampilkan detail permukiman, akses layanan, dan bantuan pemerintah.[1]

***

## 12. Dashboard Individu

Dashboard individu harus mengagregasi data dari `dataIndividu`.[1]

### 12.1 KPI utama individu
1. Total individu
2. % laki-laki
3. % perempuan
4. % peserta jaminan sosial kesehatan
5. % peserta jaminan sosial ketenagakerjaan
6. % individu usia sekolah
7. % individu bekerja
8. % individu dengan pendidikan SMA ke atas
9. % individu dengan disabilitas
10. Jumlah individu yang mengalami penyakit tertentu setahun terakhir (agregat).[1]

### 12.2 Grafik individu
Minimal tampilkan:

**Chart A — Bar**
- Distribusi pendidikan tertinggi.[1]

**Chart B — Pie/Doughnut**
- Kondisi pekerjaan: bersekolah, ibu rumah tangga, tidak bekerja, mencari pekerjaan, bekerja.[1]

**Chart C — Bar grouped**
- Peserta jaminan kesehatan vs ketenagakerjaan per lokus.[1]

**Chart D — Bar horizontal**
- Penyakit yang diderita setahun terakhir: diare, DBD, malaria, Covid-19, jantung, TBC, diabetes, dll.[1]

### 12.3 Tabel individu
Kolom minimal:
- NIK
- Nama
- Nomor KK
- Desa/Kelurahan
- Jenis kelamin
- Umur (hitung dari tanggal lahir)
- Pendidikan tertinggi
- Kondisi pekerjaan
- Peserta jaminan kesehatan
- Peserta jaminan ketenagakerjaan

Baris expandable menampilkan detail tambahan seperti bahasa, penyakit, partisipasi sosial, dan kontak digital dasar bila diisi dummy.[1]

***

## 13. Profil Tiga Lokus

Section profil harus menampilkan tiga kartu besar/tab untuk:
- Desa Malalanda
- Desa Laangke
- Kelurahan Lakonea

Isi tiap profil:
- status wilayah,
- jumlah keluarga,
- jumlah individu,
- rata-rata anggota keluarga,
- persentase rumah milik sendiri,
- persentase rumah tidak kumuh,
- persentase listrik PLN,
- persentase peserta jaminan kesehatan.[1]

Tambahkan paragraf naratif singkat 3–4 kalimat per lokus, tetapi jangan mengklaim itu data riil; nyatakan bahwa ini simulasi struktur dashboard.[1]

***

## 14. Halaman Unduh Data

Sediakan section `#unduh-data` dengan tombol berikut:

1. Unduh data keluarga — semua lokus
2. Unduh data keluarga — Malalanda
3. Unduh data keluarga — Laangke
4. Unduh data keluarga — Lakonea
5. Unduh data individu — semua lokus
6. Unduh data individu — Malalanda
7. Unduh data individu — Laangke
8. Unduh data individu — Lakonea
9. Unduh workbook gabungan (sheet keluarga + individu)

Ekspor dilakukan menggunakan **SheetJS/xlsx** di browser. Workbook gabungan harus memiliki sheet:
- `KELUARGA_ALL`
- `INDIVIDU_ALL`
- atau sheet per wilayah untuk tiap jenis data

Baris pertama harus berisi disclaimer: `DATA SIMULASI - BELUM HASIL PENDATAAN LAPANGAN RESMI`.[1]

***

## 15. Tentang Data

Section `#tentang-data` harus menjelaskan secara eksplisit:

- sumber struktur data berasal dari **kuesioner SDGs Desa Rumah Tangga** dan **Kuesioner Individu** terbaru,[1]
- unit observasi utama adalah keluarga/rumah tangga,[1]
- data individu adalah data turunan terkait anggota keluarga,[1]
- website saat ini menggunakan dummy data,[1]
- struktur database dan dashboard sudah menyesuaikan instrumen final.[1]

Tambahkan blok metadata seperti ini:

- **Lokus:** Desa Malalanda, Desa Laangke, Kelurahan Lakonea
- **Kabupaten:** Buton Utara
- **Provinsi:** Sulawesi Tenggara
- **Unit observasi utama:** Keluarga/Rumah Tangga
- **Entitas turunan:** Individu
- **Instrumen:** Kuesioner Rumah Tangga dan Kuesioner Individu SDGs Desa
- **Status data:** Simulasi / Prototype
- **Periode dummy:** 2025

***

## 16. Gaya Visual

### Arah desain
Desain harus terlihat:
- modern,
- profesional,
- data-driven,
- ringan,
- mudah dipahami oleh atasan non-teknis.

### Referensi rasa
Rasa visual tetap boleh terinspirasi website Desa Cantik lain dan situs profil desa, tetapi hasil akhir harus lebih modern, lebih bersih, dan lebih kuat pada dashboard statistik.[2][3][4]

### Palet warna
Gunakan nuansa hijau-biru-putih yang memberi kesan institusional, segar, dan dekat dengan identitas statistik publik.

```css
:root {
  --color-bg: #f6f8f7;
  --color-surface: #ffffff;
  --color-surface-2: #f1f6f3;
  --color-border: #d7e2db;
  --color-text: #193126;
  --color-text-muted: #5f7569;
  --color-primary: #176a4d;
  --color-primary-hover: #11513b;
  --color-accent: #1f8fc8;
  --color-warning: #c7781f;
  --color-success: #1e9e57;
  --color-error: #cc3a3a;
}
```

### Tipografi
- Display: `Plus Jakarta Sans`
- Body: `Inter`
- Body minimum 16px
- Data labels minimum 12px

### Logo
Buat SVG logo inline berbentuk monogram **DC** atau simbol rumah + chart sederhana untuk menegaskan tema keluarga/statistik.

***

## 17. Stack Teknis

Gunakan stack berikut:

| Kebutuhan | Pilihan |
|---|---|
| Struktur halaman | Single HTML file |
| Styling | CSS murni + CSS variables |
| Interaktivitas | Vanilla JavaScript |
| Chart | Chart.js CDN |
| Excel export | SheetJS CDN |
| Icons | Lucide CDN |
| Font | Google Fonts |

Script CDN yang bisa dipakai:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
```

***

## 18. Struktur JavaScript Aplikasi

Gunakan struktur umum seperti ini:

```javascript
const dataKeluarga = [...];
const dataIndividu = [...];

let filterWilayah = 'Semua Lokus';
let searchKeyword = '';

function getFilteredKeluarga() {
  return dataKeluarga.filter(item => {
    const matchWilayah = filterWilayah === 'Semua Lokus' || item.desa_kelurahan === filterWilayah;
    const keyword = searchKeyword.toLowerCase();
    const matchKeyword = !keyword ||
      item.nomor_kk.toLowerCase().includes(keyword) ||
      item.nama_responden.toLowerCase().includes(keyword);
    return matchWilayah && matchKeyword;
  });
}

function getFilteredIndividu() {
  const keluargaAktif = getFilteredKeluarga();
  const kkAktif = new Set(keluargaAktif.map(k => k.nomor_kk));
  return dataIndividu.filter(ind => kkAktif.has(ind.nomor_kk));
}

function renderAll() {
  renderBeranda();
  renderDashboardKeluarga();
  renderDashboardIndividu();
  renderTabelKeluarga();
  renderTabelIndividu();
}
```

***

## 19. Komponen UI Wajib

### Header
- logo SVG,
- nama situs,
- nav menu,
- tombol dark mode,
- badge `PROTOTYPE`.

### Banner simulasi
Harus ada banner yang sangat jelas di beranda dan dashboard:  
`⚠️ Data simulasi untuk prototype. Struktur sesuai kuesioner final, nilai belum hasil pendataan lapangan.`

### KPI cards
Semua KPI harus berupa card konsisten dengan icon, label, angka utama, dan keterangan kecil.

### Tabel expandable
Baik tabel keluarga maupun individu harus mendukung expand row untuk menampilkan detail tambahan.

### Tombol unduh
Tombol unduh harus besar, jelas, dan dibedakan antara dataset keluarga dan individu.

***

## 20. Responsivitas

Website wajib bagus di:
- mobile 375px,
- tablet 768px,
- desktop 1280px.

### Mobile rules
- nav collapse jadi hamburger,
- KPI cards 2 kolom,
- chart full-width,
- tabel bisa scroll horizontal,
- tombol unduh full width,
- filter dropdown stacked.

***

## 21. Aksesibilitas

- semantic HTML wajib,
- satu H1 per halaman,
- heading hierarchy rapi,
- semua tombol icon ada `aria-label`,
- fokus keyboard terlihat,
- kontras WCAG AA,
- `prefers-reduced-motion` dihormati,
- semua gambar punya `alt`.

***

## 22. Anti-Pattern yang Harus Dihindari

AI agent **jangan** membuat website yang:
- hanya cantik tetapi tidak mengikuti struktur kuesioner keluarga dan individu,[1]
- masih berpusat pada RT sebagai unit observasi utama,[1]
- menampilkan terlalu banyak indikator acak yang tidak ada di instrumen,[1]
- memakai dummy data yang tidak realistis, misalnya keluarga kecil dengan anggota individu tidak sinkron,[1]
- mengklaim angka sebagai data resmi lapangan.[1]

***

## 23. Deliverable Final yang Harus Dibuat oleh Agent

Agent harus menghasilkan:

1. **Satu file HTML utama**: `desa-cantik-buton-utara-keluarga.html`
2. Website lengkap dengan semua section berjalan
3. Data dummy keluarga dan individu sudah tertanam di file
4. Filter wilayah aktif
5. Dashboard keluarga aktif
6. Dashboard individu aktif
7. Ekspor Excel aktif
8. Dark mode aktif
9. Layout responsif
10. Label simulasi jelas

***

## 24. Checklist Final untuk Agent

### Data
- [ ] Unit observasi utama = keluarga/rumah tangga
- [ ] Ada dataset turunan individu
- [ ] Relasi keluarga–individu menggunakan nomor KK
- [ ] 30 keluarga dummy dibuat
- [ ] 120 individu dummy dibuat
- [ ] Tiga lokus terwakili
- [ ] Dummy value realistis dan sinkron

### Dashboard keluarga
- [ ] KPI keluarga tampil
- [ ] Chart keluarga tampil
- [ ] Tabel keluarga tampil dan expandable
- [ ] Filter wilayah mengubah seluruh komponen

### Dashboard individu
- [ ] KPI individu tampil
- [ ] Chart individu tampil
- [ ] Tabel individu tampil dan expandable
- [ ] Agregasi individu mengikuti filter wilayah keluarga

### Unduh data
- [ ] Tombol unduh keluarga berfungsi
- [ ] Tombol unduh individu berfungsi
- [ ] Tombol unduh workbook gabungan berfungsi
- [ ] Header Excel dan disclaimer benar

### UX/UI
- [ ] Logo SVG ada
- [ ] Sticky header ada
- [ ] Dark mode ada
- [ ] Mobile layout bagus
- [ ] Warna konsisten
- [ ] Tipografi konsisten
- [ ] Banner data simulasi terlihat jelas

### Teknis
- [ ] Tidak memakai localStorage/sessionStorage
- [ ] Tidak fetch file lokal
- [ ] Semua library via CDN
- [ ] Semantic HTML benar
- [ ] Semua komponen render tanpa error JS

***

## 25. Instruksi Inti untuk Agent

Bangun website prototype Desa Cantik untuk Kabupaten Buton Utara dengan orientasi **statistik keluarga dan individu**, bukan statistik RT. Gunakan struktur data yang setia pada kuesioner SDGs Desa Rumah Tangga dan Individu terbaru. Tampilkan dashboard yang informatif, profesional, mudah dipahami atasan, dan siap ditukar dari dummy data ke data riil tanpa perlu merombak struktur aplikasi.[1]

Website harus terasa seperti produk yang sudah matang secara arsitektur, bukan mockup kosong. Fokus pada kualitas struktur data, keterbacaan dashboard, serta kejelasan bahwa ini masih prototype berbasis simulasi.[1]