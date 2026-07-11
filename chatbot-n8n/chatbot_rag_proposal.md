# Proposal & Analisis: Adaptasi SAKERNAS RAG untuk Chatbot Desa Cantik

Alur kerja (workflow) n8n yang Anda bagikan (`SAKERNAS RAG...`) adalah sistem RAG (Retrieval-Augmented Generation) yang sangat canggih dan robust. Sistem ini memiliki klasifikasi intent, query planner (multi-path splitter), reranker hybrid berbasis kode JavaScript, mekanisme auto-retry, dan integrasi WhatsApp via WAHA.

Berikut adalah analisis mendalam dan rekomendasi cara mengadaptasi arsitektur ini untuk program **Desa Cantik** menggunakan data dari Google Spreadsheet.

---

## 1. Perbedaan Karakteristik Data & Solusinya

Sebelum mengubah alur n8n, kita harus memahami perbedaan mendasar antara data SAKERNAS dan data Desa Cantik:

| Aspek | SAKERNAS RAG (Asli) | Desa Cantik Chatbot (Rencana Anda) |
| :--- | :--- | :--- |
| **Jenis Data** | **Tak Terstruktur (Unstructured)**<br>Buku pedoman wawancara, definisi konsep pengangguran, teks panduan. | **Terstruktur (Structured)**<br>Baris data keluarga di Google Sheets (nama, NIK, status rumah, bansos, disabilitas). |
| **Metode Retrieval** | **Vector Search (Supabase)**<br>Mencari potongan teks manual yang paling mirip secara semantik. | **Database Query / Aggregation**<br>Menghitung (sum/count), memfilter, dan mendaftar data tabel. |
| **Kelemahan RAG Tradisional** | Sangat baik untuk menjawab pertanyaan konseptual ("Apa definisi bekerja?"). | Sangat buruk untuk menghitung angka ("Berapa jumlah penerima BLT di Desa Laangke?"). |

### Rekomendasi Solusi Hybrid
Agar chatbot Anda pintar dan bisa menjawab **dua tipe pertanyaan** tersebut, kita harus membuat chatbot dengan kemampuan **Hybrid Agent** (menggunakan n8n LangChain Tools):

1. **Tool A: Tanya Pedoman (Vector RAG)**
   - Jika user bertanya definisi variabel atau cara pengisian kuesioner ("Apa kriteria rumah kayu?", "Apa syarat BPJS PBI?").
   - Data bersumber dari PDF Pedoman SDGs Desa / Desa Cantik yang di-chunk dan di-upload ke Supabase Vector Store (persis seperti alur SAKERNAS asli).
2. **Tool B: Tanya Data Statistik (Google Sheets / API PHP)**
   - Jika user bertanya tentang angka data riil warga ("Berapa warga miskin di Lakonea?", "Siapa saja penerima PKH di Malalanda?").
   - AI tidak menembak vector store, melainkan memicu fungsi/API untuk membaca spreadsheet atau file PHP (`api/data.php`) untuk memfilter data secara dinamis.

---

## 2. Peta Penyesuaian Node n8n

Berikut adalah bagian-bagian di dalam file `.json` n8n Anda yang wajib disesuaikan:

### A. Node `LLM Intent Classifier3` (Baris 114)
Promp sistem di node ini harus diganti total. Dari yang sebelumnya mendeteksi konsep ketenagakerjaan SAKERNAS, diganti menjadi mendeteksi variabel profil keluarga Desa Cantik.

* **Sebelumnya (SAKERNAS):** Klasifikasi seputar `pengangguran`, `bekerja 1 jam`, `migrasi risen`, `asrama`, `KBLI/KBJI`.
* **Sesudahnya (Desa Cantik):** Klasifikasi seputar:
  - **Tabel Keluarga:** `status rumah`, `jenis atap/dinding/lantai`, `sumber air minum`, `fasilitas BAB`, `bansos (PKH, BPJS PBI, BLT)`.
  - **Tabel Lokus/Sosial:** `tingkat pendidikan`, `agama`, `jenis disabilitas`, `lapangan usaha`.

### B. Node `ANSWER-TYPE HYBRID RERANKER` (Baris 225)
Ini adalah script JavaScript kustom untuk meranking dokumen. Di dalamnya terdapat daftar kata kunci (*keywords*) dan *signals* khusus SAKERNAS. Anda harus mengganti variabel signals tersebut:

```javascript
// Ganti sinyal boundary & exception SAKERNAS menjadi variabel Desa Cantik
const descanSignals = {
  penerima_bansos: ["pkh", "bpjs pbi", "blt desa", "bantuan sosial", "menerima bantuan"],
  kondisi_rumah: ["atap rumbia", "dinding bambu", "lantai tanah", "layak huni", "tidak layak huni"],
  fasilitas_sanitasi: ["air minum", "mandi cuci kakus", "mck", "bab", "jamban sendiri"],
  kategori_lokus: ["pendidikan", "disabilitas", "lapangan usaha", "agama"]
};
```

### C. Menghubungkan Google Sheets ke LangChain Agent
Di dalam workflow SAKERNAS, LangChain Agent terhubung ke Vector Store. Agar chatbot bisa membaca data dari Google Sheets secara langsung, Anda perlu menambahkan **LangChain Tool** baru di n8n:
1. Hubungkan node **`HTTP Request`** atau **`Google Sheets Tool`** ke node LangChain Agent.
2. Beri nama tool tersebut, misalnya: `Query_Data_Desa`.
3. Beri deskripsi ke LLM: *"Gunakan tool ini untuk mendapatkan data statistik warga (seperti jumlah KK, daftar penerima bantuan, tipe rumah) untuk desa Laangke, Lakonea, dan Malalanda."*
4. Ketika ada pertanyaan tentang data, LLM akan otomatis memanggil tool ini untuk mengambil data CSV dari server atau Google Sheets, lalu merangkum jawabannya untuk user.

---

## 3. Langkah Rekomendasi Selanjutnya

1. **Gunakan Google Sheets yang "Clean":** Pastikan Google Sheets yang dibaca chatbot n8n adalah versi publik (tanpa NIK dan Nama lengkap) agar chatbot tidak membocorkan PII (Personally Identifiable Information) warga ke WhatsApp publik.
2. **Dokumen Pedoman:** Kumpulkan file PDF/Word pedoman SDGs Desa / Desa Cantik Buton Utara, lalu masukkan ke database Supabase (RAG) untuk melayani Q&A seputar teori kuesioner.
3. **Uji Coba Alur:** Saya dapat membantu Anda menulis ulang prompts sistem di n8n JSON ini dan memodifikasi script Reranker-nya agar siap di-import ke n8n Anda.

Bagaimana menurut Anda? Apakah Anda ingin chatbot ini fokus menjawab **teori pedoman pendataan** saja, atau Anda juga ingin agar dia bisa **menjawab statistik data warga** langsung dari Spreadsheet?
