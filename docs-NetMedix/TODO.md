# TODO — NetMedix

Step-by-step progress tracker. Setiap task ditandai `[x]` selesai, `[ ]` belum, `[-]` in-progress.

---

## State Proyek Saat Ini

**Status**: Phase 0-13 selesai (v1.0 stable). Semua fitur inti berjalan.

**Fitur yang sudah berjalan:**
- Landing page, diagnosis wizard (3 step), result page, history, about, admin CRUD
- Inference engine: Forward Chaining + Certainty Factor (15 rules, 40 gejala, 15 masalah)
- SQLite database untuk riwayat diagnosis
- Responsive UI (Tailwind + Lucide Icons)

**Masalah yang hendak diatasi:**
- Kombinasi gejala yang tidak cocok dengan rule manapun → halaman result kosong tanpa bantuan alternatif
- Perlu fitur "Tanyakan AI" sebagai fallback ke LLM API

**Dokumen referensi riset:** `04_TUGAS/2026-06-08_fitur-tanyakan-ai-netmedix.md`

---

## Dependency Graph & Parallel Analysis

### Tabel Dependency Antar Phase

| Phase | Nama | Dependensi | Bisa Paralel? | Dengan Phase |
|-------|------|-----------|---------------|--------------|
| **A** | Setup Environment & Config | Tidak ada | Ya | B |
| **B** | Backend API — AI Functions | Tidak ada | Ya | A |
| **C** | Backend API — Flask Route `/api/ask-ai` | **B** selesai | Tidak | — |
| **D** | Frontend — UI Tombol & Container | Tidak ada | Ya | A, B |
| **E** | Frontend — JavaScript AJAX Logic | **C** + **D** selesai | Tidak | — |
| **F** | Security & Rate Limiting | **C** selesai | Ya | E |
| **G** | Testing & Integrasi | **E** + **F** selesai | Tidak | — |
| **H** | Dokumentasi Update | **G** selesai | Tidak | — |

### Visual Dependency Graph

```
Phase A ──┐                    Phase B ──┐
(Env/CFG) │                    (AI Func) │
          ├─► Phase C ───────────────────┤
          │   (Route /api/ask-ai)        │
Phase D ──┘                             │
(UI HTML)                               │
          ├─► Phase E ──────────────────►├─► Phase F ─┐
          │   (JS AJAX)                  │   (Security)│
          │                              │             │
          │                              └─► Phase G ◄─┘
          │                                  (Testing)
          │                                      │
          │                                      ▼
          └──────────────────────────────► Phase H
                                           (Docs)
```

### Ringkasan Eksekusi Paralel

| Urutan Eksekusi | Phase | Catatan |
|-----------------|-------|---------|
| **Wave 1** (paralel) | **A** + **B** + **D** | Tidak ada dependency, bisa dikerjakan bersamaan |
| **Wave 2** (sekuen) | **C** | Butuh B selesai (AI functions sudah ada) |
| **Wave 3** (paralel) | **E** + **F** | E butuh C+D selesai; F butuh C selesai |
| **Wave 4** (sekuen) | **G** | Butuh semua phase sebelumnya selesai |
| **Wave 5** (sekuen) | **H** | Update dokumentasi setelah testing |

---

## Phase A — Setup Environment & Configuration

**Tujuan**: Menyiapkan dependency Python, environment variable, dan konfigurasi API provider.

**File yang diubah**: `requirements.txt`, `.env` (baru), `.gitignore` (sudah ada `.env`)

- [ ] A.1 — Update `requirements.txt`
  - [ ] Tambahkan `google-genai>=1.0.0` (untuk Google Gemini API)
  - [ ] Tambahkan `python-dotenv>=1.0.0` (untuk `.env` file)
  - [ ] Tambahkan `markdown>=3.4` (opsional, untuk render response markdown)
- [ ] A.2 — Install dependency baru
  - [ ] Jalankan `pip install google-genai python-dotenv markdown` di venv
  - [ ] Verifikasi: `python -c "from google import genai; print('OK')"`
- [ ] A.3 — Buat file `.env` di root project (`/04_TUGAS/NetMedix/`)
  - [ ] Tambahkan `GEMINI_API_KEY=your_api_key_here` (placeholder)
  - [ ] Tambahkan `AI_PROVIDER=gemini`
  - [ ] Verifikasi `.env` sudah ada di `.gitignore` (sudah ada)
- [ ] A.4 — Dapatkan API key dari Google AI Studio
  - [ ] Buka `ai.google.dev` → "Get API Key"
  - [ ] Copy API key ke `.env`
  - [ ] Test: `echo $GEMINI_API_KEY` dari terminal (setelah `source .env` atau `export`)
- [ ] A.5 — Validasi konfigurasi
  - [ ] Jalankan Flask app → pastikan tidak ada import error
  - [ ] Cek console: tidak ada error terkait `google.genai`

---

## Phase B — Backend: AI Service Functions

**Tujuan**: Membuat fungsi-fungsi untuk memanggil LLM API (Gemini + Groq) yang terpisah dari route logic.

**File yang diubah**: `app.py` (tambah section baru)

- [ ] B.1 — Tambah import baru di `app.py`
  - [ ] `import html` (untuk output sanitization)
  - [ ] `import re` (untuk output sanitization)
  - [ ] `import time` (untuk rate limiting)
  - [ ] `from flask import jsonify` (sudah ada di baris 5, verifikasi)
- [ ] B.2 — Tambah konfigurasi environment di bagian atas `app.py` (setelah `ADMIN_PASSWORD`)
  - [ ] Variabel `AI_PROVIDER = os.environ.get("AI_PROVIDER", "gemini")`
  - [ ] Load `.env` dengan `dotenv.load_dotenv()` (jika menggunakan python-dotenv)
- [ ] B.3 — Buat fungsi `_build_symptoms_text(symptom_names, cf_values)`
  - [ ] Accept 2 list: nama gejala dan nilai CF
  - [ ] Return string formatted: `"- {name} (tingkat keyakinan user: {cf})"` per baris
- [ ] B.4 — Buat fungsi `_build_ai_prompt(symptoms_text)`
  - [ ] System role: ahli jaringan komputer
  - [ ] Context: aplikasi NetMedix, gejala tidak tercover knowledge base
  - [ ] Output format: Kemungkinan Masalah, Penjelasan, Solusi
  - [ ] Constraint: bahasa Indonesia, fokus jaringan, praktis
- [ ] B.5 — Buat fungsi `ask_ai_gemini(symptom_names, cf_values)`
  - [ ] Import `from google import genai` (lazy import)
  - [ ] Inisialisasi client: `client = genai.Client()`
  - [ ] Gunakan model `gemini-2.0-flash`
  - [ ] Error handling: try/except, return dict `{"success": bool, ...}`
  - [ ] Return format: `{"success": True, "answer": str, "provider": "Google Gemini"}`
- [ ] B.6 — Buat fungsi `ask_ai_groq(symptom_names, cf_values)` (opsional, alternatif)
  - [ ] Import `from openai import OpenAI` (lazy import)
  - [ ] Inisialisasi client dengan `base_url="https://api.groq.com/openai/v1"`
  - [ ] Model: `llama-3.3-70b-versatile`
  - [ ] Return format: `{"success": True, "answer": str, "provider": "Groq (Llama 3.3 70B)"}`
- [ ] B.7 — Buat fungsi `_sanitize_ai_output(text)`
  - [ ] Escape HTML dengan `html.escape()`
  - [ ] Konversi markdown yang aman (bold, italic, headers, lists)
  - [ ] Return sanitized HTML string
- [ ] B.8 — Buat fungsi `_sanitize_input(symptoms_data, kb)`
  - [ ] Validasi setiap kode gejala terhadap knowledge base
  - [ ] Pastikan CF value numeric dan dalam range [-1.0, 1.0]
  - [ ] Return cleaned dict

---

## Phase C — Backend: Flask Route `/api/ask-ai`

**Tujuan**: Membuat API endpoint yang menerima request dari frontend dan mengembalikan hasil AI.

**Depends on**: Phase B selesai

**File yang diubah**: `app.py`

- [ ] C.1 — Buat route `POST /api/ask-ai/<int:session_id>`
  - [ ] Ambil `session_id` dari URL parameter
  - [ ] Load session dari DB: `get_session_by_id(session_id)`
  - [ ] Validasi session exists → 404 jika tidak
  - [ ] Parse `symptoms_selected` dan `results` dari JSON
- [ ] C.2 — Tambah guard: hanya izinkan jika `results` kosong
  - [ ] Jika `results` tidak kosong → return 400 `{"error": "Sistem pakar sudah menemukan diagnosis"}`
  - [ ] Alasan: AI hanya untuk fallback, bukan sebagai alternatif diagnosis normal
- [ ] C.3 — Ambil nama gejala dari knowledge base
  - [ ] Loop `symptoms_selected`, panggil `kb.get_symptom_by_code(code)`
  - [ ] Kumpulkan `symptom_names` dan `cf_values` sebagai list terpisah
- [ ] C.4 — Dispatch ke AI provider
  - [ ] Cek `AI_PROVIDER` env variable
  - [ ] Jika `"groq"` → panggil `ask_ai_groq()`
  - [ ] Default → panggil `ask_ai_gemini()`
- [ ] C.5 — Sanitize output AI
  - [ ] Panggil `_sanitize_ai_output()` pada `answer` sebelum return
- [ ] C.6 — Return JSON response
  - [ ] Format: `{"success": True, "answer": str, "provider": str}`
  - [ ] Error format: `{"success": False, "error": str}`
  - [ ] Gunakan `jsonify()` dari Flask

---

## Phase D — Frontend: UI Tombol & Container

**Tujuan**: Modifikasi halaman result untuk menampilkan tombol "Tanyakan AI" dan container untuk hasil AI.

**File yang diubah**: `templates/result.html`

- [ ] D.1 — Modifikasi blok `{% if not has_results %}` (saat ini baris 19-44)
  - [ ] Pertahankan header "Tidak Ada Diagnosis yang Cocok"
  - [ ] Pertahankan daftar gejala yang dipilih (badge chips)
  - [ ] Tambahkan deskripsi text yang lebih baik
- [ ] D.2 — Tambah tombol "Tanyakan AI"
  - [ ] Style: gradient purple-to-indigo (diferensiasi dari tombol primary hijau)
  - [ ] Icon: Lucide `sparkles`
  - [ ] `onclick="askAI()"` — memanggil JavaScript function
  - [ ] ID: `btn-ask-ai`
- [ ] D.3 — Tambah container AI response (hidden by default)
  - [ ] Wrapper: `id="ai-response-container"`, class `hidden`
  - [ ] Border purple, background purple-50
  - [ ] Header: icon `bot` + text "Analisis AI" + provider badge
  - [ ] Disclaimer box (yellow): penjelasan bahwa ini hasil AI, bukan sistem pakar
  - [ ] Content area: `id="ai-response-content"` untuk render jawaban AI
- [ ] D.4 — Tambah container error (hidden by default)
  - [ ] Wrapper: `id="ai-error-container"`, class `hidden`
  - [ ] Border red, background red-50
  - [ ] Icon `alert-circle` + error message text
  - [ ] `id="ai-error-message"` untuk dynamic text
- [ ] D.5 — Tambah loading state (hidden by default)
  - [ ] Wrapper: `id="ai-loading"`, class `hidden`
  - [ ] Spinner SVG (animate-spin dari Tailwind)
  - [ ] Text: "AI sedang menganalisis gejala Anda..."
- [ ] D.6 — Reorganisasi tombol bawah
  - [ ] Tombol "Tanyakan AI" di tengah (primary action saat no results)
  - [ ] Tombol "Diagnosis Lagi" di bawah (secondary action)

---

## Phase E — Frontend: JavaScript AJAX Logic

**Tujuan**: Menambahkan JavaScript untuk menangani klik tombol "Tanyakan AI" dan komunikasi dengan backend.

**Depends on**: Phase C (route harus ada) + Phase D (DOM elements harus ada)

**File yang diubah**: `templates/result.html`

- [ ] E.1 — Tambah `<script>` block di bagian bawah `result.html` (sebelum `{% endblock %}`)
  - [ ] Letakkan setelah script `cf-detail-toggle` yang sudah ada
- [ ] E.2 — Implementasi `askAI()` async function
  - [ ] Ambil referensi semua DOM elements (btn, loading, containers)
  - [ ] Reset state: disable button, show loading, hide containers
  - [ ] `fetch('/api/ask-ai/{{ session_id }}', { method: 'POST' })`
  - [ ] Handle response: parse JSON
  - [ ] Jika `data.success` → render answer ke `ai-response-content`
  - [ ] Jika `!data.success` → tampilkan error message
  - [ ] Catch network errors → tampilkan error message
  - [ ] Finally: re-enable button, hide loading
- [ ] E.3 — Implementasi `simpleMarkdown(text)` helper
  - [ ] Escape HTML entities (& < >)
  - [ ] Konversi `**bold**` → `<strong>`
  - [ ] Konversi `*italic*` → `<em>`
  - [ ] Konversi `### heading` → `<h4>`
  - [ ] Konversi `1. item` → `<li>` (ordered)
  - [ ] Konversi `- item` → `<li>` (unordered)
  - [ ] Konversi `\n\n` → `<br><br>`
- [ ] E.4 — Re-initialize Lucide icons setelah dynamic content
  - [ ] Panggil `lucide.createIcons()` setelah AI response di-render
  - [ ] Pastikan icon di container AI juga di-render

---

## Phase F — Security & Rate Limiting

**Tujuan**: Menambahkan proteksi terhadap abuse API endpoint.

**Depends on**: Phase C selesai

**File yang diubah**: `app.py`

- [ ] F.1 — Implementasi simple in-memory rate limiter
  - [ ] Variabel global: `_ai_request_times = {}`
  - [ ] Logic: max 5 request per menit per IP
  - [ ] Return 429 jika limit tercapai: `"Terlalu banyak request. Tunggu sebentar."`
  - [ ] Cleanup: hapus entry yang sudah > 60 detik
- [ ] F.2 — Integrasi rate limiter ke route `/api/ask-ai`
  - [ ] Tambah rate limit check di awal fungsi `ask_ai()`
  - [ ] Gunakan `request.remote_addr` sebagai key
- [ ] F.3 — Input validation di route
  - [ ] Panggil `_sanitize_input()` pada `symptoms_selected`
  - [ ] Hanya izinkan gejala yang valid dari knowledge base
  - [ ] Pastikan semua CF value numeric
- [ ] F.4 — Output sanitization
  - [ ] Pastikan `_sanitize_ai_output()` dipanggil di route sebelum return
  - [ ] Cegah XSS dari AI response yang mengandung `<script>` tags
- [ ] F.5 — API key validation di startup (opsional tapi bagus)
  - [ ] Cek `GEMINI_API_KEY` exists saat app start
  - [ ] Print warning ke console jika tidak ada: `"WARNING: GEMINI_API_KEY not set. Fitur AI tidak akan berfungsi."`
  - [ ] Jangan crash app — biarkan tetap jalan, fitur AI saja yang disabled

---

## Phase G — Testing & Integrasi

**Tujuan**: Memastikan semua fitur berjalan end-to-end dan edge cases tertangani.

**Depends on**: Phase E + F selesai

- [ ] G.1 — Test: environment setup
  - [ ] Verifikasi `google-genai` terinstall di venv
  - [ ] Verifikasi `.env` berisi API key yang valid
  - [ ] Verifikasi Flask app berjalan tanpa error
- [ ] G.2 — Test: skenario utama (happy path)
  - [ ] Buka `/diagnose`, pilih kombinasi gejala yang TIDAK cocok dengan rule manapun
    - Contoh: pilih G01 saja, atau G15 + G30 (kombinasi lintas kategori tanpa rule)
  - [ ] Set CF, proses diagnosis
  - [ ] Verifikasi: halaman result menampilkan "Tidak Ada Diagnosis yang Cocok"
  - [ ] Verifikasi: tombol "Tanyakan AI" muncul
  - [ ] Klik "Tanyakan AI"
  - [ ] Verifikasi: loading spinner muncul
  - [ ] Verifikasi: AI response muncul setelah 2-5 detik
  - [ ] Verifikasi: disclaimer muncul di atas hasil AI
  - [ ] Verifikasi: provider badge menunjukkan "Google Gemini"
- [ ] G.3 — Test: skenario diagnosis normal (tidak terpengaruh fitur baru)
  - [ ] Buka `/diagnose`, pilih gejala yang cocok dengan rule (misal G04 + G21 + G24 → P03)
  - [ ] Proses diagnosis
  - [ ] Verifikasi: hasil FC+CF normal ditampilkan
  - [ ] Verifikasi: tombol "Tanyakan AI" TIDAK muncul
  - [ ] Verifikasi: riwayat tersimpan normal
- [ ] G.4 — Test: error handling
  - [ ] Test dengan API key tidak valid → verifikasi error message muncul
  - [ ] Test dengan network error → verifikasi error message muncul
  - [ ] Test klik "Tanyakan AI" berkali-kali → verifikasi rate limiting bekerja
  - [ ] Test akses `/api/ask-ai/<session_id>` langsung via browser → verifikasi 405 (GET not allowed)
  - [ ] Test akses `/api/ask-ai/99999` (session tidak ada) → verifikasi 404
  - [ ] Test akses `/api/ask-ai/<session_with_results>` → verifikasi 400
- [ ] G.5 — Test: UI/UX
  - [ ] Tombol "Tanyakan AI" terlihat jelas dan menarik
  - [ ] Loading state smooth (spinner + text)
  - [ ] AI response terformat rapi (bold, lists, headers)
  - [ ] Error state terlihat jelas (merah)
  - [ ] Disclaimer box terlihat dan mudah dibaca
  - [ ] Responsif di mobile (375px) dan desktop (1440px)
  - [ ] Lucide icons di container AI terender dengan benar
- [ ] G.6 — Test: riwayat dengan hasil AI
  - [ ] Buat diagnosis → dapat hasil kosong → klik "Tanyakan AI"
  - [ ] Buka `/history`
  - [ ] Verifikasi: entry muncul dengan label "Tidak ada diagnosis"
  - [ ] Klik "Lihat Detail"
  - [ ] Verifikasi: halaman result tetap menampilkan gejala + tombol AI
- [ ] G.7 — Test: security
  - [ ] Rate limiting: kirim 6 request dalam 1 menit → request ke-6 harus 429
  - [ ] XSS prevention: cek page source AI response → tidak ada raw HTML/JS
  - [ ] Input validation: coba manipulasi session_id → harus 404/400

---

## Phase H — Dokumentasi Update

**Tujuan**: Update dokumentasi proyek untuk mencerminkan fitur baru.

**Depends on**: Phase G selesai (testing lulus)

**File yang diubah**: `docs/TODO.md`, `docs/SRS.md`, `docs/DESIGN.md`, `README.md`

- [ ] H.1 — Update `docs/TODO.md`
  - [ ] Tandai semua phase A-G sebagai `[x]` selesai
  - [ ] Tambah section "Phase A-H — Fitur Tanyakan AI"
- [ ] H.2 — Update `docs/SRS.md` (Software Requirements Specification)
  - [ ] Tambah requirement: "Sistem harus menyediakan fallback AI ketika knowledge base tidak menghasilkan diagnosis"
  - [ ] Tambah requirement: "Hasil AI harus memiliki disclaimer yang jelas"
  - [ ] Tambah API endpoint: `/api/ask-ai/<session_id>`
- [ ] H.3 — Update `docs/DESIGN.md`
  - [ ] Tambah color token untuk AI section (purple palette)
  - [ ] Tambah komponen: AI response card, disclaimer box, loading spinner
- [ ] H.4 — Update `README.md`
  - [ ] Update "Fitur" section: tambahkan "AI Fallback (Tanyakan AI)"
  - [ ] Update "Requirements" section: tambah `google-genai`
  - [ ] Tambah section "Konfigurasi AI": cara setup API key
  - [ ] Tambah arsitektur diagram hybrid (rule-based + LLM fallback)
- [ ] H.5 — Update `docs/VERSION-CONTROL.md`
  - [ ] Tambah entry: `v1.1.0 — Fitur Tanyakan AI (hybrid expert system + LLM fallback)`

---

## Quick Reference: File yang Diubah Per Phase

| File | Phase | Perubahan |
|------|-------|-----------|
| `requirements.txt` | A | Tambah `google-genai`, `python-dotenv`, `markdown` |
| `.env` (baru) | A | API key + config |
| `app.py` | B, C, F | Import, AI functions, route `/api/ask-ai`, rate limiter, sanitization |
| `templates/result.html` | D, E | Tombol AI, containers, JS `askAI()` |
| `docs/TODO.md` | H | Update status |
| `docs/SRS.md` | H | Tambah requirements |
| `docs/DESIGN.md` | H | Tambah AI color tokens |
| `docs/VERSION-CONTROL.md` | H | Tambah versi |
| `README.md` | H | Update fitur & setup |

---

## Phase Sebelumnya (v1.0 — Selesai)

<details>
<summary>Klik untuk melihat Phase 0-13 (sudah selesai)</summary>

### Phase 0 — Planning & Research ✅
- [x] Riset domain troubleshooting jaringan komputer
- [x] Kompilasi 15 masalah jaringan (P01-P15)
- [x] Kompilasi 40 gejala (G01-G40)
- [x] Buat knowledge base matrix (gejala × masalah)
- [x] Definisikan 15 aturan IF-THEN (R01-R15)
- [x] Finalisasi nilai MB/MD untuk setiap gejala per aturan
- [x] Buat contoh perhitungan CF (3 skenario)
- [x] Tulis SRS (Software Requirements Specification)
- [x] Tulis PRD (Product Requirements Document)

### Phase 1 — Project Setup ✅
- [x] Inisialisasi folder project
- [x] Setup Python venv + Flask 3.x
- [x] Setup Tailwind via CDN di base template
- [x] Setup Google Fonts (Inter) via CDN
- [x] Setup Lucide Icons via CDN
- [x] Test: Flask dev server berjalan

### Phase 2 — Knowledge Base (Data Layer) ✅
- [x] Buat `data/problems.json` — 15 masalah jaringan lengkap
- [x] Buat `data/symptoms.json` — 40 gejala lengkap
- [x] Buat `data/rules.json` — 15 aturan + MB/MD values
- [x] Validasi konsistensi kode antara files

### Phase 3 — Inference Engine ✅
- [x] Buat `inference/knowledge_base.py`
- [x] Buat `inference/engine.py` (Forward Chaining + CF)
- [x] Unit test manual: verifikasi 3 skenario

### Phase 4 — Base Template & Navigation ✅
- [x] Buat `templates/base.html`
- [x] Buat `static/js/app.js`
- [x] Test: base template render

### Phase 5 — Landing Page ✅
- [x] Buat `templates/index.html`
- [x] Hero, cara kerja, kategori, statistik sections

### Phase 6 — Diagnosis Wizard Step 1 ✅
- [x] Buat `templates/diagnose.html`
- [x] Kategori tabs, checkbox, counter, validation

### Phase 7 — Diagnosis Wizard Step 2 ✅
- [x] Buat `templates/diagnose_step2.html`
- [x] CF level radio buttons, summary bar

### Phase 8 — Diagnosis Wizard Step 3 ✅
- [x] Buat `templates/result.html`
- [x] Result cards, CF progress bar, detail expandable

### Phase 9 — Riwayat Diagnosis ✅
- [x] SQLite setup (`init_db`, `save_session`, CRUD)
- [x] Buat `templates/history.html`

### Phase 10 — Halaman Tentang ✅
- [x] Buat `templates/about.html`
- [x] Forward Chaining, Certainty Factor, arsitektur, referensi

### Phase 11 — Admin Panel ✅
- [x] Login, dashboard, CRUD problems/symptoms/rules
- [x] Session-based auth, `@login_required` decorator

### Phase 12 — Polish & Responsive ✅
- [x] Responsive semua halaman
- [x] Konsistensi visual
- [x] Error handling (404, 500, flash messages)
- [x] Loading state, empty states, accessibility

### Phase 13 — End-to-End Testing ✅
- [x] Functional testing (semua flow)
- [x] 6 skenario diagnosis manual (semua PASS)
- [x] Cross-browser testing
- [x] Responsive testing
- [x] Final review

</details>
