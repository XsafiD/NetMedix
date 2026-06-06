# NetMedix

**Sistem Pakar Diagnosis Masalah Jaringan Komputer** menggunakan metode **Forward Chaining** dan **Certainty Factor**.

Proyek UAS mata kuliah Sistem Cerdas — Semester 4 Informatika.

---

## Tentang

NetMedix adalah aplikasi web yang membantu pengguna mengidentifikasi masalah jaringan komputer berdasarkan gejala-gejala yang dialami. Pengguna memilih gejala, menentukan tingkat keyakinan, dan sistem menghitung diagnosis menggunakan metode Certainty Factor (CF) dengan inferensi Forward Chaining.

### Fitur Utama

- **Diagnosis 3 Langkah** — pilih gejala, tentukan keyakinan, lihat hasil
- **15 masalah jaringan** dalam 7 kategori (Konektivitas, DNS, DHCP, WiFi, Performa, Keamanan, Hardware)
- **40 gejala** yang dapat dipilih pengguna
- **15 aturan IF-THEN** dengan nilai MB/MD per gejala
- **Detail perhitungan CF** — menampilkan step-by-step evidence dan kombinasi CF
- **Riwayat diagnosis** — tersimpan di SQLite, bisa dilihat dan dihapus
- **Admin Panel** — CRUD knowledge base (masalah, gejala, aturan) tanpa edit JSON manual
- **Responsif** — desktop, tablet, mobile

---

## Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Backend | Python 3.10+ / Flask 3.x |
| Frontend CSS | Tailwind CSS 3.x (CDN) |
| Frontend JS | Vanilla JavaScript |
| Font | Inter (Google Fonts) |
| Icons | Lucide Icons (CDN) |
| Template | Jinja2 (bundled with Flask) |
| Knowledge Base | JSON files |
| Database | SQLite 3 (Python stdlib) |

Zero build step. Semua dependensi frontend via CDN.

---

## Instalasi & Menjalankan

### Prasyarat

- Python 3.10 atau lebih baru

### Langkah

```bash
# 1. Clone atau masuk ke direktori project
cd NetMedix

# 2. Buat virtual environment (jika belum ada)
python3 -m venv venv

# 3. Aktifkan venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 4. Install dependensi
pip install flask

# 5. Jalankan aplikasi
python app.py
```

Buka browser ke **http://localhost:5000**

---

## Struktur Proyek

```
NetMedix/
├── app.py                    # Flask entry point (routes, DB, auth)
├── inference/
│   ├── __init__.py
│   ├── engine.py             # Forward Chaining + Certainty Factor
│   └── knowledge_base.py     # JSON loader & query methods
├── data/
│   ├── problems.json          # 15 masalah jaringan (P01-P15)
│   ├── symptoms.json          # 40 gejala (G01-G40)
│   └── rules.json             # 15 aturan IF-THEN + MB/MD (R01-R15)
├── templates/
│   ├── base.html              # Base layout
│   ├── index.html             # Landing page
│   ├── diagnose.html          # Step 1 — Pilih Gejala
│   ├── diagnose_step2.html    # Step 2 — Tingkat Keyakinan
│   ├── result.html            # Step 3 — Hasil Diagnosis
│   ├── about.html             # Tentang sistem
│   ├── history.html           # Riwayat diagnosis
│   ├── 404.html / 500.html    # Error pages
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── problems.html      # CRUD masalah
│       ├── symptoms.html      # CRUD gejala
│       └── rules.html         # CRUD aturan
├── static/js/app.js           # Client-side JS
├── database/                  # SQLite (auto-created)
└── venv/
```

---

## Metode

### Forward Chaining

Metode inferensi data-driven: sistem memulai dari fakta (gejala yang dipilih) dan mencocokkan dengan aturan IF-THEN di knowledge base. Jika semua gejala dalam sebuah aturan terpenuhi, aturan tersebut "terpicu" dan menghasilkan diagnosis.

### Certainty Factor (CF)

Mengukur tingkat keyakinan terhadap diagnosis menggunakan tiga rumus:

**1. CF Rule** — keyakinan pakar terhadap aturan:
```
CF(H,E) = MB - MD
```

**2. CF Evidence** — gabungan keyakinan pakar dan user:
```
CF_evidence = CF_user × CF(H,E)
```

**3. CF Combine** — kombinasi beberapa evidence:
```
CF_combine = CF1 + CF2 × (1 - CF1)
```

### Contoh Perhitungan

Diagnosis "Koneksi Internet Terputus" (P02) dengan input G02=0.8, G03=1.0, G28=0.6:

| Gejala | MB | MD | CF Rule | CF User | CF Evidence |
|--------|----|----|---------|---------|-------------|
| G02    | 0.8 | 0.1 | 0.70  | 0.80    | 0.560       |
| G03    | 0.9 | 0.1 | 0.80  | 1.00    | 0.800       |
| G28    | 0.9 | 0.1 | 0.80  | 0.60    | 0.480       |

```
Step 1: CF1 = 0.560
Step 2: combine(0.560, 0.800) = 0.560 + 0.800 × 0.440 = 0.912
Step 3: combine(0.912, 0.480) = 0.912 + 0.480 × 0.088 = 0.9542
```

**Hasil: P02 — Koneksi Internet Terputus, CF = 95.42%**

---

## Knowledge Base

### Masalah Jaringan (15)

| Kategori | Masalah |
|----------|---------|
| Konektivitas Dasar | P01 Tidak Ada Koneksi, P02 Internet Terputus |
| DNS | P03 Resolution Failure, P04 Cache Poisoning |
| DHCP & IP Config | P05 DHCP Failure, P06 IP Conflict, P07 Subnet/Gateway Salah |
| WiFi | P08 Tidak Bisa Connect, P09 Signal Lemah |
| Performa | P10 Jaringan Lambat, P11 Packet Loss, P12 Latensi Tinggi |
| Keamanan | P13 Firewall Memblokir |
| Hardware | P14 Kerusakan Kabel, P15 Kerusakan Router/Switch |

### Gejala (40)

Tersebar di 7 kategori: Konektivitas (11), DNS (4), DHCP & IP Config (6), WiFi (4), Performa (5), Keamanan (4), Hardware (6).

---

## Halaman

| Route | Deskripsi |
|-------|-----------|
| `/` | Landing page — hero, cara kerja, kategori, statistik |
| `/diagnose` | Step 1 — pilih gejala (tab per kategori) |
| `/diagnose/step2` | Step 2 — tentukan tingkat keyakinan (9 level) |
| `/result/<id>` | Step 3 — hasil diagnosis + detail perhitungan CF |
| `/history` | Riwayat semua diagnosis |
| `/about` | Penjelasan metode Forward Chaining & Certainty Factor |
| `/admin/login` | Login admin (default: admin / admin123) |
| `/admin` | Dashboard admin |
| `/admin/problems` | CRUD masalah jaringan |
| `/admin/symptoms` | CRUD gejala |
| `/admin/rules` | CRUD aturan IF-THEN + MB/MD |

---

## Admin Panel

Login default:

```
Username: admin
Password: admin123
```

Melalui admin panel, knowledge base dapat dikelola tanpa mengedit file JSON secara manual. Perubahan langsung berpengaruh ke diagnosis.

---

## Dokumentasi Tambahan

| File | Isi |
|------|-----|
| `SRS.md` | Software Requirements Specification |
| `PRD.md` | Product Requirements Document |
| `DESIGN.md` | Design system reference |
| `TODO.md` | Step-by-step task tracker (all done) |
| `VERSION-CONTROL.md` | Version history & changelog |

---

## Referensi

- Kusumadewi, S. (2003). *Artificial Intelligence (Teknik Pengembangan Komputasi)*. Graha Ilmu.
- Negnevitsky, M. (2024). *Artificial Intelligence: A Guide to Intelligent Systems* (4th ed.). Pearson.
- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Shortliffe, E.H. & Buchanan, B.G. (1975). "A model of inexact reasoning in medicine." *Mathematical Biosciences*.
- CompTIA Network+ (N10-008) — referensi domain troubleshooting jaringan.

---

*NetMedix v1.0.0 — Proyek UAS Sistem Cerdas 2026*
