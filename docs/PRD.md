# Product Requirements Document (PRD)

## NetMedix — Sistem Pakar Troubleshooting Jaringan Komputer

**Versi:** 1.0
**Tanggal:** 2026-06-06
**Owner:** Tim Sistem Cerdas

---

## 1. Product Vision

NetMedix adalah aplikasi web yang membantu pengguna mendiagnosis masalah jaringan komputer secara mandiri menggunakan sistem pakar berbasis aturan (rule-based expert system). Aplikasi ini menerapkan metode **Forward Chaining** untuk pencocokan gejala dan **Certainty Factor** untuk menghitung tingkat keyakinan diagnosis.

### Value Proposition

> "Diagnosis masalah jaringan dalam hitungan detik — tanpa perlu jadi ahli IT."

### Target User

| Segment | Prioritas |
|---------|-----------|
| Mahasiswa Informatika (evaluasi UAS) | P0 — Utama |
| Pengguna awam dengan masalah jaringan | P1 |
| Teknisi junior jaringan | P2 |

---

## 2. Tech Stack

| Layer | Teknologi | Versi | Delivery |
|-------|-----------|-------|----------|
| **Backend** | Python + Flask | 3.10+, Flask 3.x | venv (`venv/bin/pip install flask`) |
| **Frontend** | HTML + Tailwind CSS + Vanilla JS | Tailwind 3.x | CDN (cdnjs / cdn.tailwindcss.com) |
| **Template Engine** | Jinja2 (via Flask) | — | bundled Flask |
| **Knowledge Base** | JSON file | — | local file |
| **History Storage** | SQLite | 3.x | Python stdlib |
| **Icons** | Lucide Icons | latest | CDN (unpkg.com) |
| **Font** | Inter (Google Fonts) | — | CDN (fonts.googleapis.com) |
| **Deployment** | Local (Flask dev server) | — | `venv/bin/python app.py` |

### CDN Dependencies

```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Google Fonts: Inter -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<!-- Lucide Icons -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
```

### Project Structure

```
NetMedix/
├── app.py                  # Flask application entry point
├── inference/
│   ├── engine.py           # Forward Chaining + CF calculation
│   └── knowledge_base.py   # KB loader & manager
├── data/
│   ├── problems.json       # 15 masalah jaringan
│   ├── symptoms.json       # 40 gejala
│   └── rules.json          # 15 aturan IF-THEN + MB/MD
├── templates/
│   ├── base.html           # Base layout (Tailwind + CDN)
│   ├── index.html          # Landing page
│   ├── diagnose.html       # Halaman diagnosis
│   ├── result.html         # Halaman hasil diagnosis
│   ├── history.html        # Riwayat diagnosis
│   ├── about.html          # Tentang / penjelasan metode
│   └── admin/
│       ├── login.html      # Admin login
│       ├── dashboard.html  # Admin dashboard
│       ├── problems.html   # CRUD masalah
│       ├── symptoms.html   # CRUD gejala
│       └── rules.html      # CRUD aturan
├── static/
│   └── js/
│       └── app.js          # Client-side interactivity
├── database/
│   └── history.db          # SQLite untuk riwayat
├── SRS.md                  # Software Requirements Specification
├── PRD.md                  # Product Requirements Document (this file)
├── DESIGN.md               # Design system reference
└── 2026-06-06_riset-troubleshooting-jaringan-komputer.md
```

---

## 3. Design Language

Seluruh UI mengikuti panduan di `DESIGN.md` dengan adaptasi berikut:

### 3.1 Token Mapping ke Tailwind

| DESIGN.md Token | Tailwind Class | Hex |
|------------------|----------------|-----|
| `{colors.canvas}` | `bg-white` | `#ffffff` |
| `{colors.canvas-soft}` | `bg-[#fafafa]` | `#fafafa` |
| `{colors.canvas-night}` | `bg-[#1c1c1c]` | `#1c1c1c` |
| `{colors.primary}` | `bg-[#3ecf8e]` | `#3ecf8e` |
| `{colors.primary-deep}` | `bg-[#24b47e]` | `#24b47e` |
| `{colors.ink}` | `text-[#171717]` | `#171717` |
| `{colors.ink-mute}` | `text-[#707070]` | `#707070` |
| `{colors.ink-faint}` | `text-[#b2b2b2]` | `#b2b2b2` |
| `{colors.hairline}` | `border-[#dfdfdf]` | `#dfdfdf` |
| `{colors.on-primary}` | `text-[#171717]` | `#171717` |
| `{colors.on-dark}` | `text-white` | `#ffffff` |

### 3.2 Tailwind Config Override

```javascript
tailwind.config = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
        mono: ['ui-monospace', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      colors: {
        canvas: '#ffffff',
        'canvas-soft': '#fafafa',
        'canvas-night': '#1c1c1c',
        primary: '#3ecf8e',
        'primary-deep': '#24b47e',
        ink: '#171717',
        'ink-mute': '#707070',
        'ink-faint': '#b2b2b2',
        hairline: '#dfdfdf',
      },
      borderRadius: {
        btn: '6px',
        card: '12px',
      },
    },
  },
}
```

### 3.3 Komponen Utama

#### Button Primary (CTA)
```html
<button class="bg-primary text-ink font-medium text-sm px-4 py-2 rounded-btn
               hover:bg-primary-deep transition-colors">
  Mulai Diagnosis
</button>
```

#### Card Gejala
```html
<div class="bg-white p-6 rounded-card border border-hairline hover:border-primary
            transition-colors cursor-pointer">
  <label class="flex items-start gap-3 cursor-pointer">
    <input type="checkbox" class="mt-1 accent-[#3ecf8e]">
    <div>
      <p class="font-medium text-ink">G01 — Tidak ada koneksi</p>
      <p class="text-sm text-ink-mute">Apakah perangkat Anda tidak bisa terhubung?</p>
    </div>
  </label>
</div>
```

#### Result Card
```html
<div class="bg-white p-8 rounded-card border border-hairline">
  <div class="flex items-center gap-3 mb-4">
    <span class="text-2xl font-semibold text-ink">95.4%</span>
    <span class="bg-primary text-ink text-xs font-medium px-2 py-0.5 rounded-full">
      Sangat Yakin
    </span>
  </div>
  <h3 class="text-lg font-medium text-ink">P02 — Koneksi Internet Terputus</h3>
  <p class="text-ink-mute mt-2">Jaringan lokal berfungsi, tetapi tidak bisa akses internet.</p>
  <div class="mt-4 pt-4 border-t border-hairline">
    <h4 class="font-medium text-ink text-sm mb-2">Solusi:</h4>
    <ul class="text-sm text-ink-mute space-y-1">
      <li>1. Restart router</li>
      <li>2. Cek kabel WAN</li>
      <li>3. Hubungi ISP</li>
    </ul>
  </div>
</div>
```

#### Navigation Bar
```html
<nav class="bg-white border-b border-hairline px-6 py-4">
  <div class="max-w-5xl mx-auto flex items-center justify-between">
    <a href="/" class="font-semibold text-ink text-lg">
      Net<span class="text-primary">Medix</span>
    </a>
    <div class="flex items-center gap-6 text-sm font-medium text-ink-mute">
      <a href="/diagnose" class="hover:text-ink transition-colors">Diagnosis</a>
      <a href="/history" class="hover:text-ink transition-colors">Riwayat</a>
      <a href="/about" class="hover:text-ink transition-colors">Tentang</a>
      <a href="/admin" class="bg-primary text-ink px-4 py-2 rounded-btn text-sm
                              hover:bg-primary-deep transition-colors">Admin</a>
    </div>
  </div>
</nav>
```

### 3.4 Prinsip Visual

1. **White canvas** — background utama selalu putih. Tidak ada gradient atmosferik.
2. **Emerald sparse** — warna primary `#3ecf8e` hanya untuk CTA button, pill tag keyakinan, dan logo accent.
3. **Near-black on green** — teks di tombol primary menggunakan `#171717`, bukan putih.
4. **Hairline borders** — semua card dan separator menggunakan `border-[#dfdfdf]` 1px.
5. **Negative tracking** — heading menggunakan `tracking-tight` (letter-spacing negatif).
6. **Square-ish buttons** — radius 6px, tidak pernah pill-shaped.

---

## 4. Fitur dan Halaman

### 4.1 Landing Page (`/`)

**Tujuan:** Memberikan first impression dan mengarahkan user ke diagnosis.

**Sections:**
1. **Hero** — judul "NetMedix", tagline, CTA "Mulai Diagnosis"
2. **Cara Kerja** — 3 langkah: Pilih Gejala → Tentukan Keyakinan → Lihat Hasil
3. **Kategori Masalah** — 7 kategori (Konektivitas, DNS, DHCP, WiFi, Performa, Keamanan, Hardware) dalam grid card
4. **Statistik** — 15 masalah, 40 gejala, metode CF

### 4.2 Diagnosis Page (`/diagnose`)

**Tujuan:** Inti aplikasi — user memilih gejala dan mendapat diagnosis.

**Alur 3-step wizard:**

**Step 1 — Pilih Gejala:**
- Gejala dikelompokkan dalam 7 kategori.
- Setiap gejala ditampilkan sebagai card dengan checkbox.
- User bisa memilih 1-15 gejala.
- Counter menunjukkan jumlah gejala terpilih.
- Button "Lanjutkan" aktif jika minimal 1 gejala dipilih.

**Step 2 — Tentukan Keyakinan:**
- Untuk setiap gejala yang dipilih di Step 1, tampilkan card dengan 9 opsi tingkat keyakinan.
- Default: "Tidak Tahu" (0.2).
- Visual: radio button group horizontal atau dropdown.
- Button "Proses Diagnosis" untuk submit.

**Step 3 — Hasil Diagnosis:**
- Tampilkan 1-3 diagnosis teratas, diurutkan berdasarkan CF tertinggi.
- Setiap result card menampilkan:
  - Persentase CF (dengan progress bar)
  - Label keyakinan (Sangat Yakin / Cukup Yakin / Kemungkinan / dll.)
  - Nama dan deskripsi masalah
  - Daftar penyebab
  - Daftar solusi (langkah perbaikan)
- Jika CF tertinggi < 0.40, tampilkan warning: "Diagnosis kurang pasti. Pertimbangkan untuk menambah gejala atau konsultasi teknisi."
- Button "Diagnosis Lagi" dan "Simpan ke Riwayat".

### 4.3 History Page (`/history`)

**Tujuan:** Menampilkan riwayat sesi diagnosis.

**Tampilan:**
- Tabel/card list dengan kolom: tanggal, jumlah gejala, diagnosis utama, persentase CF.
- Klik item untuk expand/melihat detail lengkap.
- Button "Hapus Riwayat".

### 4.4 About Page (`/about`)

**Tujuan:** Edukasi tentang metode yang digunakan.

**Sections:**
1. **Tentang NetMedix** — deskripsi aplikasi
2. **Forward Chaining** — penjelasan dengan diagram sederhana
3. **Certainty Factor** — penjelasan rumus CF, MB, MD
4. **Arsitektur Sistem** — diagram blok komponen
5. **Referensi** — daftar jurnal dan textbook

### 4.5 Admin Panel (`/admin`)

**Tujuan:** Manajemen knowledge base.

**Autentikasi:**
- Login sederhana dengan username/password (hardcoded di config).
- Session-based (Flask session).

**Dashboard:**
- Statistik: jumlah masalah, gejala, aturan.
- Quick links ke CRUD setiap entitas.

**CRUD Tables:**
- **Problems** — tabel dengan kolom: kode, nama, kategori. Klik row untuk edit.
- **Symptoms** — tabel dengan kolom: kode, deskripsi, kategori. Klik row untuk edit.
- **Rules** — tabel dengan kolom: kode, gejala (list), target masalah, MB/MD. Form multi-row untuk input gejala + MB/MD per aturan.

---

## 5. API Routes

| Method | Route | Fungsi |
|--------|-------|--------|
| GET | `/` | Landing page |
| GET | `/diagnose` | Halaman diagnosis (Step 1: pilih gejala) |
| POST | `/diagnose/step2` | Step 2: tentukan keyakinan |
| POST | `/diagnose/process` | Proses inferensi, redirect ke result |
| GET | `/result/<session_id>` | Halaman hasil diagnosis |
| GET | `/history` | Daftar riwayat diagnosis |
| GET | `/history/<id>` | Detail riwayat |
| DELETE | `/history/<id>` | Hapus riwayat |
| GET | `/about` | Halaman tentang |
| GET | `/admin/login` | Form login admin |
| POST | `/admin/login` | Proses login admin |
| GET | `/admin` | Admin dashboard |
| GET | `/admin/problems` | CRUD masalah |
| POST | `/admin/problems` | Tambah masalah |
| PUT | `/admin/problems/<id>` | Edit masalah |
| DELETE | `/admin/problems/<id>` | Hapus masalah |
| GET | `/admin/symptoms` | CRUD gejala |
| POST | `/admin/symptoms` | Tambah gejala |
| PUT | `/admin/symptoms/<id>` | Edit gejala |
| DELETE | `/admin/symptoms/<id>` | Hapus gejala |
| GET | `/admin/rules` | CRUD aturan |
| POST | `/admin/rules` | Tambah aturan |
| PUT | `/admin/rules/<id>` | Edit aturan |
| DELETE | `/admin/rules/<id>` | Hapus aturan |

---

## 6. Data Model

### 6.1 JSON Knowledge Base

**`data/problems.json`**
```json
[
  {
    "code": "P01",
    "name": "Tidak Ada Koneksi Jaringan",
    "category": "Konektivitas Dasar",
    "description": "Perangkat tidak terhubung ke jaringan sama sekali...",
    "causes": ["NIC disabled", "kabel putus", "..."],
    "solutions": ["Cek NIC", "Ganti kabel", "..."]
  }
]
```

**`data/symptoms.json`**
```json
[
  {
    "code": "G01",
    "description": "Tidak ada koneksi sama sekali",
    "question": "Apakah perangkat Anda tidak bisa terhubung ke jaringan sama sekali?",
    "category": "Konektivitas"
  }
]
```

**`data/rules.json`**
```json
[
  {
    "code": "R01",
    "symptoms": [
      {"code": "G01", "mb": 0.9, "md": 0.1},
      {"code": "G20", "mb": 0.8, "md": 0.1},
      {"code": "G26", "mb": 0.7, "md": 0.1}
    ],
    "conclusion": "P01"
  }
]
```

### 6.2 SQLite Schema (History)

```sql
CREATE TABLE diagnosis_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    symptoms_selected TEXT NOT NULL,       -- JSON: [{"code": "G01", "cf_user": 0.8}, ...]
    results TEXT NOT NULL,                  -- JSON: [{"problem": "P01", "cf_final": 0.95}, ...]
    top_diagnosis TEXT NOT NULL,            -- problem code
    top_cf REAL NOT NULL                    -- CF value
);
```

---

## 7. Milestones

| Phase | Deliverable | Status |
|-------|-------------|--------|
| Riset | Dokumen riset + knowledge base | Done |
| Spec | SRS + PRD | Done |
| Core | Inference engine (FC + CF) + KB loader | [ ] |
| UI | Landing + Diagnosis wizard + Result page | [ ] |
| History | Riwayat diagnosis (SQLite) | [ ] |
| Admin | Admin panel + CRUD knowledge base | [ ] |
| About | Halaman tentang + dokumentasi metode | [ ] |
| Polish | Responsive + final styling + testing | [ ] |

---

## 8. Success Metrics

| Metrik | Target |
|--------|--------|
| Akurasi diagnosis | ≥ 85% dibanding teknisi |
| Waktu diagnosis rata-rata | ≤ 3 menit per sesi |
| Bug kritis | 0 pada demo UAS |
| Halaman responsif | 100% halaman mobile-friendly |
