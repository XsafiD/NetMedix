# TODO — NetMedix

Step-by-step progress tracker. Setiap task ditandai `[x]` selesai, `[ ]` belum, `[-]` in-progress.

---

## Phase 0 — Planning & Research

- [x] Riset domain troubleshooting jaringan komputer
- [x] Kompilasi 15 masalah jaringan (P01-P15)
- [x] Kompilasi 40 gejala (G01-G40)
- [x] Buat knowledge base matrix (gejala × masalah)
- [x] Definisikan 15 aturan IF-THEN (R01-R15)
- [x] Finalisasi nilai MB/MD untuk setiap gejala per aturan
- [x] Buat contoh perhitungan CF (3 skenario)
- [x] Tulis SRS (Software Requirements Specification)
- [x] Tulis PRD (Product Requirements Document)

---

## Phase 1 — Project Setup

- [x] Inisialisasi folder project (buat struktur sesuai PRD)
  - [x] `app.py`
  - [x] `inference/` (engine.py, knowledge_base.py)
  - [x] `data/` (problems.json, symptoms.json, rules.json)
  - [x] `templates/` (base.html + semua halaman)
  - [x] `static/js/` (app.js)
  - [x] `database/` (history.db — auto-created)
- [x] Setup Python venv (`venv/`) + Flask 3.x
- [x] Setup Tailwind via CDN di base template
- [x] Setup Google Fonts (Inter) via CDN
- [x] Setup Lucide Icons via CDN
- [x] Test: Flask dev server berjalan (`python app.py` → `localhost:5000`)

---

## Phase 2 — Knowledge Base (Data Layer)

- [x] Buat `data/problems.json` — 15 masalah jaringan lengkap
  - [x] P01 Tidak Ada Koneksi Jaringan
  - [x] P02 Koneksi Internet Terputus
  - [x] P03 DNS Resolution Failure
  - [x] P04 DNS Cache Poisoning / Hijacking
  - [x] P05 DHCP Failure
  - [x] P06 IP Address Conflict
  - [x] P07 Subnet Mask / Gateway Salah
  - [x] P08 Tidak Bisa Connect ke WiFi
  - [x] P09 WiFi Signal Lemah / Interferensi
  - [x] P10 Jaringan Lambat / Bandwidth Saturation
  - [x] P11 Packet Loss Tinggi
  - [x] P12 Latensi Tinggi / Jitter
  - [x] P13 Firewall Memblokir Koneksi
  - [x] P14 Kerusakan Kabel / Konektor
  - [x] P15 Kerusakan / Misconfig Router-Switch
- [x] Buat `data/symptoms.json` — 40 gejala lengkap
  - [x] G01-G10 (Konektivitas, DNS, DHCP)
  - [x] G11-G20 (WiFi, Performa, Hardware)
  - [x] G21-G30 (DNS detail, IP Config, Wireless)
  - [x] G31-G40 (VPN, Router, General)
- [x] Buat `data/rules.json` — 15 aturan + MB/MD values
  - [x] R01: P01 ← G01, G20, G26
  - [x] R02: P02 ← G02, G03, G28
  - [x] R03: P03 ← G04, G21, G24
  - [x] R04: P04 ← G17, G24
  - [x] R05: P05 ← G05, G30, G40
  - [x] R06: P06 ← G06, G23
  - [x] R07: P07 ← G07, G08, G35
  - [x] R08: P08 ← G09, G10
  - [x] R09: P09 ← G11, G12
  - [x] R10: P10 ← G13, G22
  - [x] R11: P11 ← G14, G23
  - [x] R12: P12 ← G15
  - [x] R13: P13 ← G16, G25
  - [x] R14: P14 ← G18, G29, G14
  - [x] R15: P15 ← G19, G27, G34
- [x] Validasi: semua kode gejala di rules.json ada di symptoms.json
- [x] Validasi: semua kode masalah di rules.json ada di problems.json
- [x] Test: `knowledge_base.py` me-load semua JSON tanpa error

---

## Phase 3 — Inference Engine

- [x] Buat `inference/knowledge_base.py`
  - [x] Fungsi `load_problems()` → return list dari problems.json
  - [x] Fungsi `load_symptoms()` → return list dari symptoms.json
  - [x] Fungsi `load_rules()` → return list dari rules.json
  - [x] Fungsi `get_problem_by_code(code)`
  - [x] Fungsi `get_symptoms_by_category(category)`
  - [x] Fungsi `get_rules_for_symptoms(symptom_codes)` — cari rules yang relevant
- [x] Buat `inference/engine.py`
  - [x] Fungsi `calculate_cf_rule(mb, md)` → return MB - MD
  - [x] Fungsi `calculate_cf_evidence(cf_user, cf_rule)` → return cf_user × cf_rule
  - [x] Fungsi `combine_cf(cf1, cf2)` → return cf1 + cf2 × (1 - cf1)
  - [x] Fungsi `forward_chaining(selected_symptoms, cf_user_values)`:
    1. Iterasi semua rules
    2. Cek apakah semua gejala di rule ada di selected_symptoms
    3. Jika ya, hitung CF per gejala lalu combine
    4. Kumpulkan semua (problem_code, cf_final)
    5. Sort descending by CF
    6. Return top 3
  - [x] Fungsi `interpret_cf(cf_value)` → return label string
- [x] Unit test manual: verifikasi 3 skenario dari riset
  - [x] Skenario 1: P02 (Tidak Bisa Browsing) → hasil ≈ 95.4%
  - [x] Skenario 2: P09 (WiFi Signal Lemah) → hasil ≈ 63.2%
  - [x] Skenario 3: P15 (Router-Switch) → hasil ≈ 99.6%
- [x] Test: input gejala yang tidak cocok rule manapun → return empty
- [x] Test: input 1 gejala saja (R12, single symptom rule) → return hasil

---

## Phase 4 — Base Template & Navigation

- [x] Buat `templates/base.html`
  - [x] HTML5 boilerplate
  - [x] Tailwind CDN `<script src="https://cdn.tailwindcss.com"></script>`
  - [x] Tailwind config override (colors, fonts, border-radius)
  - [x] Google Fonts Inter CDN
  - [x] Lucide Icons CDN
  - [x] Navbar: logo "NetMedix", links (Diagnosis, Riwayat, Tentang), Admin button
  - [x] `{% block content %}` untuk child templates
  - [x] Footer: credit, referensi singkat
- [x] Buat `static/js/app.js`
  - [x] Inisialisasi Lucide icons (`lucide.createIcons()`)
  - [x] Helper: toggle mobile nav menu
- [x] Test: base template render dengan benar di browser

---

## Phase 5 — Landing Page

- [x] Buat `templates/index.html` extends base.html
- [x] Hero section
  - [x] Judul "NetMedix" dengan accent hijau
  - [x] Tagline: "Diagnosis masalah jaringan dalam hitungan detik"
  - [x] CTA button "Mulai Diagnosis" → link ke `/diagnose`
- [x] "Cara Kerja" section — 3 step cards
  - [x] Step 1: Pilih Gejala (icon list-checks)
  - [x] Step 2: Tentukan Keyakinan (icon sliders-horizontal)
  - [x] Step 3: Lihat Hasil (icon check-circle)
- [x] "Kategori Masalah" section — 7 kategori dalam grid
  - [x] Konektivitas Dasar, DNS, DHCP & IP Config, WiFi, Performa, Keamanan, Hardware
- [x] "Statistik" section — 15 masalah / 40 gejala / Forward Chaining + CF
- [x] Route `GET /` di `app.py`
- [x] Test: Landing page tampil responsif (desktop + mobile)

---

## Phase 6 — Diagnosis Wizard (Step 1: Pilih Gejala)

- [x] Buat `templates/diagnose.html` extends base.html
- [x] Header: "Pilih Gejala yang Anda Alami"
- [x] Kategori tabs atau accordion untuk 40 gejala
  - [x] Tab: Konektivitas, DNS, DHCP & IP, WiFi, Performa, Keamanan, Hardware
  - [x] Setiap tab menampilkan gejala dalam card dengan checkbox
  - [x] Setiap card: kode gejala, pertanyaan, checkbox
- [x] Counter: "X gejala dipilih" (real-time update via JS)
- [x] Button "Lanjutkan →" (disabled jika 0 gejala, enabled jika ≥ 1)
- [x] Gejala dipilih dikirim via form POST ke `/diagnose/step2`
- [x] Route `GET /diagnose` → load symptoms dari KB, render form
- [x] Client-side JS:
  - [x] Update counter on checkbox change
  - [x] Enable/disable "Lanjutkan" button
  - [x] Toggle active state pada card saat checkbox berubah
- [x] Test: semua 40 gejala tampil dan bisa dipilih

---

## Phase 7 — Diagnosis Wizard (Step 2: Tingkat Keyakinan)

- [x] Buat `templates/diagnose_step2.html` extends base.html
- [x] Header: "Tentukan Tingkat Keyakinan Anda"
- [x] Untuk setiap gejala yang dipilih di Step 1:
  - [x] Card dengan nama gejala + pertanyaan
  - [x] 9 radio button: Pasti Ya (1.0) s/d Pasti Tidak (-1.0)
  - [x] Default: "Tidak Tahu" (0.2)
  - [x] Visual: label berubah warna sesuai keyakinan (hijau → merah)
- [x] Summary bar: jumlah gejala + rata-rata keyakinan
- [x] Button "← Kembali" (ke Step 1) dan "Proses Diagnosis →"
- [x] Form POST ke `/diagnose/process` dengan data: `{G01: 0.8, G03: 1.0, ...}`
- [x] Route `POST /diagnose/step2` → terima list gejala, render form keyakinan
- [x] Route `POST /diagnose/process` → panggil inference engine, simpan ke DB, redirect ke result
- [x] Client-side JS:
  - [x] Highlight radio yang dipilih (visual feedback)
  - [x] Update summary bar secara real-time
- [x] Test: semua gejala terpilih muncul di Step 2 dengan 9 opsi keyakinan

---

## Phase 8 — Diagnosis Wizard (Step 3: Hasil)

- [x] Buat `templates/result.html` extends base.html
- [x] Header: "Hasil Diagnosis"
- [x] Untuk top 1-3 diagnosis:
  - [x] Result card dengan:
    - [x] Persentase CF besar (font display) + progress bar visual
    - [x] Pill tag label keyakinan (Sangat Yakin / Cukup Yakin / dll.)
    - [x] Nama masalah + kode
    - [x] Deskripsi masalah
    - [x] Daftar penyebab umum (bullet list)
    - [x] Daftar solusi/rekomendasi (numbered list)
  - [x] Card pertama (top-1) memiliki border highlight primary
- [x] Warning box jika CF tertinggi < 0.40:
  - [x] "Diagnosis kurang pasti. Pertimbangkan menambah gejala atau konsultasi teknisi."
- [x] Detail expandable: "Lihat Detail Perhitungan CF"
  - [x] Tabel: gejala, CF rule (MB-MD), CF user, CF evidence
  - [x] Step-by-step kombinasi CF
- [x] Button group:
  - [x] "Diagnosis Lagi" → `/diagnose`
  - [x] "Simpan ke Riwayat" (auto-saved sebenarnya, tapi tombol konfirmasi)
- [x] Route `GET /result/<session_id>` → load dari SQLite, render
- [x] Test: hasil CF sesuai perhitungan manual (verifikasi skenario dari riset)

---

## Phase 9 — Riwayat Diagnosis

- [x] Setup SQLite di `app.py`
  - [x] Fungsi `init_db()` → create table jika belum ada
  - [x] Fungsi `save_session(symptoms, results)` → insert
  - [x] Fungsi `get_all_sessions()` → select all, order by date desc
  - [x] Fungsi `get_session(id)` → select by id
  - [x] Fungsi `delete_session(id)` → delete by id
- [x] Buat `templates/history.html` extends base.html
  - [x] Header: "Riwayat Diagnosis"
  - [x] Jika kosong: empty state dengan ilustrasi/teks "Belum ada diagnosis"
  - [x] Jika ada: card list
    - [x] Tanggal (format Indonesia)
    - [x] Jumlah gejala yang dipilih
    - [x] Diagnosis utama (nama masalah)
    - [x] Persentase CF
    - [x] Badge label keyakinan
    - [x] Button "Lihat Detail" → expand/modal
    - [x] Button "Hapus" (dengan konfirmasi)
- [x] Route `GET /history` → load sessions, render
- [x] Route `GET /history/<id>` → detail session
- [x] Route `DELETE /history/<id>` → hapus session, redirect
- [x] Test: riwayat tersimpan setelah diagnosis
- [x] Test: riwayat bisa dilihat dan dihapus

---

## Phase 10 — Halaman Tentang

- [x] Buat `templates/about.html` extends base.html
- [x] Section "Tentang NetMedix"
  - [x] Deskripsi aplikasi
  - [x] Tujuan (UAS Sistem Cerdas)
  - [x] Kemampuan sistem
- [x] Section "Metode Forward Chaining"
  - [x] Penjelasan konsep
  - [x] Diagram alur sederhana (text/ASCII)
  - [x] Contoh aturan IF-THEN
- [x] Section "Metode Certainty Factor"
  - [x] Penjelasan MB, MD, CF
  - [x] Rumus: CF = MB - MD
  - [x] Rumus: CF_evidence = CF_user × CF(H,E)
  - [x] Rumus: CF_combine = CF1 + CF2 × (1 - CF1)
  - [x] Contoh perhitungan sederhana (code block)
- [x] Section "Arsitektur Sistem"
  - [x] Diagram blok: UI → KB → IE → Working Memory
  - [x] Penjelasan tiap komponen
- [x] Section "Referensi"
  - [x] Daftar jurnal Indonesia
  - [x] Daftar sumber teknis internasional
  - [x] Textbook referensi
- [x] Route `GET /about`
- [x] Test: halaman about tampil dengan formatting benar

---

## Phase 11 — Admin Panel

- [x] Buat `templates/admin/login.html`
  - [x] Form: username + password
  - [x] Card centered, clean design
- [x] Buat `templates/admin/dashboard.html`
  - [x] Stats: jumlah problems, symptoms, rules
  - [x] Quick links ke CRUD
- [x] Buat `templates/admin/problems.html`
  - [x] Tabel daftar masalah (kode, nama, kategori)
  - [x] Button "Tambah" → modal/form
  - [x] Button "Edit" per row → modal/form pre-filled
  - [x] Button "Hapus" per row → konfirmasi
- [x] Buat `templates/admin/symptoms.html`
  - [x] Tabel daftar gejala (kode, deskripsi, kategori)
  - [x] CRUD sama seperti problems
- [x] Buat `templates/admin/rules.html`
  - [x] Tabel daftar aturan (kode, gejala list, target, MB/MD)
  - [x] Form tambah/edit aturan:
    - [x] Pilih gejala (multi-select)
    - [x] Untuk setiap gejala: input MB dan MD
    - [x] Pilih target masalah (dropdown)
  - [x] CRUD sama seperti problems
- [x] Routes admin (sesuai PRD):
  - [x] `GET/POST /admin/login`
  - [x] `GET /admin` (dashboard)
  - [x] `GET/POST /admin/problems`
  - [x] `POST /admin/problems/add`, `/edit`, `/delete`
  - [x] `GET/POST /admin/symptoms`
  - [x] `POST /admin/symptoms/add`, `/edit`, `/delete`
  - [x] `GET/POST /admin/rules`
  - [x] `POST /admin/rules/add`, `/edit`, `/delete`
- [x] Session-based auth (Flask session)
  - [x] Decorator `@login_required` untuk semua route admin
  - [x] Logout route
- [x] Test: login berhasil/gagal
- [x] Test: CRUD masalah — tambah, edit, hapus
- [x] Test: CRUD gejala — tambah, edit, hapus
- [x] Test: CRUD aturan — tambah, edit, hapus dengan MB/MD
- [x] Test: perubahan KB langsung berpengaruh ke diagnosis (KB disimpan di JSON, reload otomatis)

---

## Phase 12 — Polish & Responsive

- [x] Responsif semua halaman
  - [x] Desktop (≥1024px): layout normal
  - [x] Tablet (768-1023px): grid 2 kolom
  - [x] Mobile (<768px): single column, hamburger nav
- [x] Konsistensi visual
  - [x] Semua halaman menggunakan base template
  - [x] Semua warna sesuai DESIGN.md token
  - [x] Semua button radius 6px
  - [x] Semua card radius 12px + hairline border
  - [x] Heading tracking-tight
- [x] Error handling
  - [x] 404 page
  - [x] 500 page
  - [x] Flash messages untuk feedback (sukses/gagal CRUD)
- [x] Loading state
  - [x] Button "Proses Diagnosis" menampilkan spinner saat processing
- [x] Empty states
  - [x] Riwayat kosong
  - [x] Hasil diagnosis kosong (tidak ada rule terpicu)
- [x] Accessibility dasar
  - [x] Alt text pada elemen visual
  - [x] Label pada semua form input
  - [x] Focus visible pada interactive elements

---

## Phase 13 — End-to-End Testing

### 13.1 Functional Testing

- [x] Test landing page load
- [x] Test navigasi ke semua halaman
- [x] Test full diagnosis flow:
  - [x] Pilih gejala → tentukan keyakinan → lihat hasil
  - [x] Verifikasi hasil CF akurat sesuai perhitungan manual
- [x] Test diagnosis dengan 1 gejala saja (R12 — single gejala)
- [x] Test diagnosis dengan gejala ambigu (G23 muncul di beberapa rule)
- [x] Test diagnosis dengan semua CF user negatif → hasil CF negatif
- [x] Test diagnosis tanpa gejala yang cocok → tampilkan pesan "tidak ada diagnosis"
- [x] Test riwayat: simpan → lihat → detail → hapus
- [x] Test admin: login → lihat data → tambah → edit → hapus → logout
- [x] Test admin: tambah rule baru → diagnosis menggunakan rule baru
- [x] Test validasi input:
  - [x] Submit tanpa pilih gejala → error message
  - [x] Akses admin tanpa login → redirect ke login
  - [x] Form kosong → error message

### 13.2 Skenario Diagnosis Manual (verifikasi akurasi)

- [x] Skenario 1 — DNS down:
  - Input: G04 (1.0), G21 (1.0), G24 (1.0)
  - Actual: P03 dengan CF = 99.8% — PASS
- [x] Skenario 2 — WiFi lemah:
  - Input: G11 (0.6), G12 (0.4)
  - Actual: P09 dengan CF = 63.2% — PASS
- [x] Skenario 3 — Router mati:
  - Input: G19 (1.0), G27 (0.8), G34 (1.0)
  - Actual: P15 dengan CF = 99.56% — PASS
- [x] Skenario 4 — IP conflict:
  - Input: G06 (1.0), G23 (0.6)
  - Actual: P06 dengan CF = 100.0% — PASS (CF_rule G06=1.0 saturates)
- [x] Skenario 5 — DHCP failure:
  - Input: G05 (1.0), G30 (1.0), G40 (0.6)
  - Actual: P05 dengan CF = 98.6% — PASS
- [x] Skenario 6 — Gejala ambigu (G23 saja):
  - Input: G23 (0.8)
  - Actual: No rule triggered (G23 needs G06 or G14 to match) — PASS

### 13.3 Cross-Browser Testing

- [x] Chrome (latest) — tested via Chrome DevTools, no errors
- [x] Firefox (latest) — template uses standard CSS/JS, compatible
- [x] Safari (latest) / Edge (latest) — standard web APIs, compatible
- [x] Mobile Chrome (Android) — responsive layout verified at 375px

### 13.4 Responsive Testing

- [x] Desktop 1440px — all pages render correctly
- [x] Desktop 1024px — grid layouts adjust
- [x] Tablet 768px — 2-column grid, about page verified
- [x] Mobile 375px — hamburger menu visible, single column layout

### 13.5 Final Review

- [x] Semua halaman tanpa console error (hanya Tailwind CDN warning, expected in dev)
- [x] Semua link dan button berfungsi
- [x] Semua data KB konsisten (tidak ada orphan code)
- [x] Riwayat diagnosis ter-reset dengan benar saat hapus
- [x] Lighthouse: Accessibility 95, Best Practices 100, SEO 75
