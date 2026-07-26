# Software Requirements Specification (SRS)

## NetMedix — Sistem Pakar Troubleshooting Jaringan Komputer

**Versi:** 1.0
**Tanggal:** 2026-06-06
**Platform:** Web Application
**Metode Inferensi:** Certainty Factor (CF)

---

## 1. Pendahuluan

### 1.1 Tujuan

Dokumen ini mendefinisikan kebutuhan fungsional dan non-fungsional untuk **NetMedix**, sebuah sistem pakar berbasis web yang mendiagnosis masalah jaringan komputer menggunakan metode Certainty Factor (CF). Sistem ditujukan untuk pengguna awam hingga teknisi junior yang membutuhkan diagnosis awal masalah jaringan.

### 1.2 Ruang Lingkup

NetMedix mendiagnosis **15 masalah jaringan** berdasarkan **40 gejala** yang dipilih oleh pengguna, dengan tingkat keyakinan diukur menggunakan Certainty Factor (CF). Sistem memberikan hasil diagnosis beserta persentase keyakinan dan rekomendasi solusi.

### 1.3 Definisi, Akronim, dan Singkatan

| Istilah | Definisi |
|---------|----------|
| CF | Certainty Factor — ukuran keyakinan net (MB - MD) |
| MB | Measure of Belief — derajat keyakinan positif (0-1) |
| MD | Measure of Disbelief — derajat keyakinan negatif (0-1) |
| KB | Knowledge Base — basis pengetahuan sistem |
| IE | Inference Engine — mesin inferensi |
| UI | User Interface — antarmuka pengguna |

### 1.4 Referensi

1. Dokumen riset: `2026-06-06_riset-troubleshooting-jaringan-komputer.md`
2. Negnevitsky, M. (2024). *Artificial Intelligence.* Ch. 2-5.
3. Kusumadewi, S. (2003). *Artificial Intelligence.* Bab 5.
4. Shortliffe & Buchanan. Certainty Factor Theory (MYCIN, 1970s).

---

## 2. Deskripsi Umum

### 2.1 Perspektif Produk

NetMedix adalah aplikasi web mandiri (standalone) yang berjalan di browser. Sistem tidak memerlukan integrasi dengan perangkat jaringan fisik — semua input berasal dari respons pengguna terhadap pertanyaan gejala.

### 2.2 Kelas dan Karakteristik Pengguna

| Kelas Pengguna | Deskripsi | Kebutuhan |
|----------------|-----------|-----------|
| Pengguna Awam | Tidak memiliki pengetahuan teknis jaringan | Antarmuka sederhana, bahasa non-teknis |
| Teknisi Junior | Memiliki pengetahuan dasar jaringan | Diagnosis cepat, detail teknis opsional |
| Mahasiswa | Pembelajaran konsep sistem pakar | Visualisasi alur inferensi, transparansi CF |
| Administrator | Mengelola basis pengetahuan | CRUD gejala, masalah, dan aturan |

### 2.3 Lingkungan Operasi

| Komponen | Spesifikasi |
|----------|-------------|
| Server | Python 3.10+, Flask |
| Browser | Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ |
| Resolusi | Minimum 375px (mobile) — optimal 1280px+ (desktop) |
| Jaringan | Dapat berjalan 100% offline (local deployment) |

---

## 3. Kebutuhan Fungsional

### 3.1 Modul Diagnosis

#### FR-01: Pemilihan Gejala
- Sistem menampilkan daftar **40 gejala** jaringan dalam bentuk checklist.
- Setiap gejala memiliki pertanyaan deskriptif dalam bahasa Indonesia.
- Pengguna memilih satu atau lebih gejala yang dialami.
- Setiap gejala yang dipilih HARUS diberi tingkat keyakinan.

#### FR-02: Tingkat Keyakinan Pengguna
- Untuk setiap gejala yang dipilih, pengguna memilih salah satu dari **9 tingkat keyakinan**:

| Label | Nilai CF |
|-------|----------|
| Pasti Ya | 1.0 |
| Hampir Pasti Ya | 0.8 |
| Kemungkinan Besar Ya | 0.6 |
| Mungkin Ya | 0.4 |
| Tidak Tahu | 0.2 |
| Mungkin Tidak | -0.4 |
| Kemungkinan Besar Tidak | -0.6 |
| Hampir Pasti Tidak | -0.8 |
| Pasti Tidak | -1.0 |

#### FR-03: Proses Inferensi
- Sistem mencocokkan gejala yang dipilih user dengan aturan IF-THEN di knowledge base.
- Aturan dengan **≥ 2 gejala relevan** yang dipilih user dianggap kandidat diagnosis (filter false positive).
- Sistem menghitung **CF evidence** untuk setiap gejala: `CF_evidence = CF_user × CF_pakar`.
- Sistem menggabungkan CF menggunakan rumus kombinasi: `CF_combine = CF1 + CF2 × (1 - CF1)`.
- Hasil akhir berupa daftar semua kandidat diagnosis yang diurutkan berdasarkan nilai CF tertinggi.

#### FR-04: Hasil Diagnosis
- Sistem menampilkan **semua kandidat diagnosis yang lolos filter ≥ 2 gejala relevan** dengan:
  - Nama masalah jaringan
  - Persentase keyakinan (CF × 100%)
  - Deskripsi masalah
  - Penyebab umum
  - Solusi/rekomendasi perbaikan (langkah-langkah)
- Interpretasi CF:

| Range CF | Label |
|----------|-------|
| 0.80 - 1.00 | Sangat Yakin |
| 0.60 - 0.79 | Cukup Yakin |
| 0.40 - 0.59 | Kemungkinan |
| 0.20 - 0.39 | Kurang Yakin |
| < 0.20 | Tidak Yakin |

#### FR-05: Riwayat Diagnosis
- Sistem menyimpan riwayat sesi diagnosis.
- Pengguna dapat melihat kembali hasil diagnosis sebelumnya.
- Riwayat mencatat: tanggal, gejala dipilih, hasil diagnosis, dan persentase CF.

### 3.2 Modul Knowledge Base

#### FR-06: Data Masalah Jaringan
- Sistem menyimpan **15 masalah jaringan** (`P01` - `P15`) meliputi:
  - Kode masalah, nama masalah, kategori, deskripsi, penyebab umum, solusi
- Data disimpan dalam format JSON.

#### FR-07: Data Gejala
- Sistem menyimpan **40 gejala** (`G01` - `G40`) meliputi:
  - Kode gejala, deskripsi gejala, pertanyaan ke pengguna
- Data disimpan dalam format JSON.

#### FR-08: Data Aturan (Rules)
- Sistem menyimpan **15 aturan IF-THEN** (`R01` - `R15`) meliputi:
  - Kode aturan, daftar gejala (antecedent), masalah target (consequent)
  - Nilai MB dan MD untuk setiap gejala dalam aturan
- Data disimpan dalam format JSON.

### 3.3 Modul Administrasi

#### FR-09: Manajemen Knowledge Base
- Administrator dapat melihat seluruh data masalah, gejala, dan aturan.
- Administrator dapat menambah, mengubah, dan menghapus data masalah, gejala, dan aturan.
- Perubahan pada knowledge base langsung berpengaruh pada proses diagnosis.

### 3.4 Modul Informasi

#### FR-10: Halaman Tentang
- Menjelaskan metode Certainty Factor (CF) secara lengkap (rumus, MB/MD, contoh perhitungan, diagram alur, contoh aturan IF-THEN).
- Menampilkan arsitektur sistem secara visual.
- Menampilkan profil pengembang dan referensi.

---

## 4. Kebutuhan Antarmuka

### 4.1 Halaman Utama (Landing)
- Hero section dengan nama aplikasi **NetMedix** dan tagline.
- CTA button "Mulai Diagnosis" menuju halaman diagnosis.
- Section penjelasan singkat tentang cara kerja sistem.
- Section kategori masalah yang bisa didiagnosis.

### 4.2 Halaman Diagnosis
- **Step 1 — Pilih Gejala:** Daftar 40 gejala dalam bentuk card-based checklist. Gejala dikelompokkan per kategori (Konektivitas, DNS, DHCP, WiFi, Performa, Keamanan, Hardware). Pengguna memilih gejala yang dialami.
- **Step 2 — Tentukan Keyakinan:** Untuk setiap gejala terpilih, pengguna memilih tingkat keyakinan dari 9 opsi (slider atau radio button group).
- **Step 3 — Hasil Diagnosis:** Menampilkan semua kandidat diagnosis yang lolos filter dengan persentase, deskripsi, dan solusi. Tombol "Diagnosis Lagi" untuk memulai sesi baru.

### 4.3 Halaman Riwayat
- Daftar riwayat diagnosis dalam format tabel/card.
- Setiap item menampilkan: tanggal, jumlah gejala, diagnosis utama, persentase CF.
- Klik item untuk melihat detail lengkap.

### 4.4 Halaman Admin
- Login sederhana (username + password hardcoded).
- CRUD table untuk masalah, gejala, dan aturan.
- Setiap entri bisa ditambah, diedit, dan dihapus.

### 4.5 Halaman Tentang
- Penjelasan metode Certainty Factor (CF) dengan diagram alur perhitungan, contoh aturan IF-THEN, dan contoh perhitungan.
- Arsitektur sistem.
- Daftar referensi.

---

## 5. Kebutuhan Non-Fungsional

### 5.1 Performa

| ID | Kebutuhan | Metrik |
|----|-----------|--------|
| NFR-01 | Waktu response diagnosis | < 2 detik dari submit gejala ke tampil hasil |
| NFR-02 | Waktu load halaman | < 3 detik pada koneksi standar |
| NFR-03 | Kapasitas knowledge base | Mendukung hingga 100 gejala dan 50 masalah |

### 5.2 Kebergunaan (Usability)

| ID | Kebutuhan |
|----|-----------|
| NFR-04 | Antarmuka sepenuhnya dalam Bahasa Indonesia |
| NFR-05 | Pengguna awam dapat menyelesaikan diagnosis tanpa bantuan dalam ≤ 5 menit |
| NFR-06 | Desain responsif untuk mobile dan desktop |
| NFR-07 | Warna dan kontras memenuhi WCAG 2.1 AA |

### 5.3 Keandalan (Reliability)

| ID | Kebutuhan |
|----|-----------|
| NFR-08 | Sistem tidak crash jika input tidak valid |
| NFR-09 | Validasi input: minimal 1 gejala harus dipilih sebelum diagnosis |
| NFR-10 | Pesan error yang jelas dan informatif |

### 5.4 Keamanan (Security)

| ID | Kebutuhan |
|----|-----------|
| NFR-11 | Halaman admin dilindungi autentikasi sederhana |
| NFR-12 | Input pengguna divalidasi di sisi server (no XSS/injection) |
| NFR-13 | Tidak ada data sensitif yang disimpan |

### 5.5 Portabilitas

| ID | Kebutuhan |
|----|-----------|
| NFR-14 | Dapat dijalankan di Windows, macOS, dan Linux |
| NFR-15 | Dapat dideploy locally (localhost) maupun cloud |

---

## 6. Constraint dan Asumsi

### 6.1 Constraint
- Knowledge base dibangun dari studi literatur internet, **tanpa wawancara langsung ke pakar**.
- Sistem tidak melakukan scan atau test jaringan secara langsung — semua input bersifat manual (user-reported).
- Target akurasi: ≥ 85% dibandingkan diagnosis teknisi jaringan.

### 6.2 Asumsi
- Pengguna memahami bahasa Indonesia.
- Pengguna dapat mengamati gejala dasar jaringan (lampu indikator, pesan error, status koneksi).
- Browser pengguna mendukung JavaScript ES6+.

---

## 7. Knowledge Base Specification

### 7.1 Struktur Data Masalah

```json
{
  "code": "P01",
  "name": "Tidak Ada Koneksi Jaringan",
  "category": "Konektivitas Dasar",
  "description": "Perangkat tidak terhubung ke jaringan sama sekali",
  "causes": ["NIC disabled", "kabel putus", "switch port mati", "driver NIC bermasalah"],
  "solutions": ["Cek NIC", "Ganti kabel", "Cek switch port", "Update driver"]
}
```

### 7.2 Struktur Data Gejala

```json
{
  "code": "G01",
  "description": "Tidak ada koneksi sama sekali",
  "question": "Apakah perangkat Anda tidak bisa terhubung ke jaringan sama sekali?",
  "category": "Konektivitas"
}
```

### 7.3 Struktur Data Aturan

```json
{
  "code": "R01",
  "symptoms": [
    {"code": "G01", "mb": 0.9, "md": 0.1},
    {"code": "G20", "mb": 0.8, "md": 0.1},
    {"code": "G26", "mb": 0.7, "md": 0.1}
  ],
  "conclusion": "P01"
}
```

### 7.4 Jumlah Data

| Entitas | Jumlah |
|---------|--------|
| Masalah (Problems) | 15 |
| Gejala (Symptoms) | 40 |
| Aturan (Rules) | 15 |

---

## 8. Algoritma Inferensi

### 8.1 Certainty Factor

```
Untuk setiap aturan R di knowledge base:
1. matched = irisan(gejala pada R, gejala yang dipilih user)
2. Jika |matched| < 2 → skip aturan R (filter false positive)

3. Untuk setiap gejala G_i dalam matched:
   CF_evidence_i = CF_user_i × CF_pakar_i   (CF_pakar dari knowledge base)

4. Kombinasikan CF_evidence secara sekuensial (fold left-to-right):
   CF_combine[1] = CF_evidence_1
   CF_combine[i] = CF_combine[i-1] + CF_evidence_i × (1 - CF_combine[i-1])

5. CF_final_R = CF_combine terakhir untuk aturan R
   Persentase keyakinan = CF_final_R × 100%

Setelah semua aturan diproses:
6. Urutkan kandidat diagnosis berdasarkan CF_final descending.
7. Kembalikan SEMUA kandidat yang lolos filter (no top-3 truncation).
```

---

## 9. Acceptance Criteria

| ID | Kriteria | Status |
|----|----------|--------|
| AC-01 | User dapat memilih gejala dan tingkat keyakinan | [ ] |
| AC-02 | Sistem menghasilkan diagnosis dengan persentase CF | [ ] |
| AC-03 | Diagnosis menampilkan solusi/rekomendasi | [ ] |
| AC-04 | Admin dapat mengelola knowledge base | [ ] |
| AC-05 | Riwayat diagnosis tersimpan dan dapat dilihat | [ ] |
| AC-06 | UI responsif di mobile dan desktop | [ ] |
| AC-07 | Perhitungan CF akurat sesuai rumus (dapat diverifikasi manual) | [ ] |
| AC-08 | Aturan terpicu dengan benar (≥ 2 gejala relevan terpenuhi) | [ ] |
