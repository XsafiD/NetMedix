---
created_at: 2026-07-09
version_target: "2.0.0"
project: "NetMedix"
topic: "TODO Tasklist Rombak NetMedix v2.0.0"
tags: [expert-system, certainty-factor, netmedix, todo, tasklist, e2e-testing]
related_files:
  - "[Perencanaan](./perencanaan-rombak-v2.0.0-NetMedix.md)"
  - "[Desain teknis](./desain-teknis-v2.0.0-NetMedix.md)"
  - "[Discussion log](../../00_INBOX/2026-07-09_discussion-rombak-netmedix-pure-cf.md)"
status: "active"
ai_model: "Claude (glm-5)"
---

# TODO Tasklist Rombak NetMedix v2.0.0

> Daftar task terperinci dari persiapan dokumen hingga testing E2E. Centang task yang sudah selesai. Update `status` di frontmatter & progress table di bagian bawah saat maju.

## Status Legend

- `[ ]` — pending
- `[~]` — in progress
- `[x]` — selesai
- `[!]` — blocked

---

## Phase 0 — Persiapan & Perencanaan

- [x] Pemanasan — pemahaman baseline v1.0.0 (engine.py, knowledge_base.py, rules.json)
- [x] Diskusi Sesi 1 — spec rombak high-level (9 keputusan locked)
- [x] Diskusi Sesi 2 — pivot ke CF_pakar langsung (5 keputusan metodologi locked)
- [x] Buat discussion log `00_INBOX/2026-07-09_discussion-rombak-netmedix-pure-cf.md`
- [x] Konfirmasi major version bump → v2.0.0
- [x] Buat `perencanaan-rombak-v2.0.0-NetMedix.md` (PRD)
- [x] Buat `desain-teknis-v2.0.0-NetMedix.md` (technical design)
- [x] Buat `todo-rombak-v2.0.0-NetMedix.md` (file ini)

---

## Phase 1 — Riset Knowledge Base (CF_pakar + Tutorial Gejala)

### Fase 1.A — Sample Validasi Metodologi (P12 & P15)

- [x] Buat `docs-NetMedix/tabel-cf-pakar-riset.md` dengan template kosong (header + 15 section P01-P15)
- [x] Riset **P12 — Latensi Tinggi/Jitter** (sample simple, single symptom G15)
  - [x] Cari ≥ 3 sumber independen tentang gejala latensi tinggi
  - [x] Tentukan CF_pakar via Opsi D (skala ordinal + engineering judgment)
  - [x] Identifikasi gejala tambahan relevan (G22 speed test rendah? G13 lambat?)
  - [x] Isi tabel P12 dengan justifikasi + sumber per nilai
  - [x] Bundling: isi short_desc, how_to_check, tutorial G15 (juga gejala tambahan kalau ada)
- [x] Riset **P15 — Kerusakan Router/Switch** (sample complex, 3 gejala G19/G27/G34)
  - [x] Cari ≥ 3 sumber per gejala (total min 9 sumber)
  - [x] Tentukan CF_pakar per gejala via Opsi D
  - [x] Identifikasi gejala tambahan relevan (G28? G33?)
  - [x] Isi tabel P15 dengan justifikasi + sumber
  - [x] Bundling: isi tutorial G19, G27, G34
- [x] **Review metodologi** setelah sample P12 & P15
  - [x] Skala ordinal terasa natural atau perlu adjust?
  - [x] Threshold "min 2 sumber per nilai" tercapai?
  - [x] Ada orphan yang ternyata relevan?
  - [x] Update discussion log dengan temuan review

### Fase 1.B — Produksi Massal 13 Penyakit Sisanya

Urutan dari yang paling mudah (gejala sedikit) ke kompleks:

- [ ] **P11 — Packet Loss Tinggi** (G14, G23)
- [ ] **P04 — DNS Cache Poisoning** (G17, G24)
- [ ] **P10 — Jaringan Lambat** (G13, G22)
- [ ] **P06 — IP Address Conflict** (G06, G23)
- [ ] **P08 — Tidak Bisa Connect WiFi** (G09, G10)
- [ ] **P09 — WiFi Signal Lemah** (G11, G12)
- [ ] **P13 — Firewall Memblokir** (G16, G25)
- [ ] **P01 — Tidak Ada Koneksi Jaringan** (G01, G20, G26)
- [ ] **P02 — Koneksi Internet Terputus** (G02, G03, G28)
- [ ] **P03 — DNS Resolution Failure** (G04, G21, G24)
- [ ] **P05 — DHCP Failure** (G05, G30, G40)
- [ ] **P07 — Subnet/Gateway Salah** (G07, G08, G35)
- [ ] **P14 — Kerusakan Kabel** (G18, G29, G14)

Tiap penyakit: riset ≥ 3 sumber + tentukan CF_pakar Opsi D + bundling tutorial gejala.

### Fase 1.C — Resolve Orphan Symptoms (G31-G39)

- [ ] Riset G31 (VPN tidak bisa connect) — relevan ke problem mana?
- [ ] Riset G32 (VPN internal gagal) — relevan?
- [ ] Riset G33 (Lampu LAN router mati) — bedakan dari G28/G18?
- [ ] Riset G36 (Network adapter disabled) — relevan ke P01?
- [ ] Riset G37 (Driver adapter bermasalah) — relevan?
- [ ] Riset G38 (Single device bermasalah) — relevan ke P01/P06?
- [ ] Riset G39 (Proxy aktif) — rule baru atau orphan permanen?
- [ ] **Keputusan per orphan:** tambah ke rule existing / buat rule baru / biarkan orphan dengan badge "belum didukung"

### Fase 1.D — Peer Review Konsistensi

- [ ] Review silang gejala cross-cutting:
  - [ ] G14 (packet loss) konsisten di P11 & P14?
  - [ ] G23 (intermittent) konsisten di P06 & P11?
  - [ ] G24 (IP only) konsisten di P03 & P04?
- [ ] Verifikasi minimal 2 sumber independen per nilai CF_pakar
- [ ] Verifikasi range CF_pakar semua [0.1, 1.0]
- [ ] Verifikasi setiap rule punya ≥ 2 symptoms
- [ ] Commit tabel CF_pakar final ke `docs-NetMedix/tabel-cf-pakar-riset.md`

### Fase 1.E — Riset Konten Tutorial per Gejala (Bundling)

> Idealnya di-bundle dengan Fase 1.B (sekali baca sumber, sekalian isi tutorial).

- [ ] 40 gejala masing-masing punya: `short_desc`, `how_to_check`, `tutorial.{definition, verification_steps, interpretation, common_causes, related_symptoms}`
- [ ] Konsistensi format steps (imperative voice: "Buka...", "Jalankan...")
- [ ] Konsistensi interpretasi (format: "X%: kategori | Y%: kategori")

---

## Phase 2 — Migrasi Data

- [ ] Backup `data/rules.json` → `data/rules.v1.0.0.json.bak`
- [ ] Backup `data/symptoms.json` → `data/symptoms.v1.0.0.json.bak`
- [ ] Port nilai CF_pakar dari `docs-NetMedix/tabel-cf-pakar-riset.md` → `rules.json` v2 schema
  - [ ] Tambah field `sources` per rule (min 2 URL)
  - [ ] Tambah field `cf_pakar` per gejala
  - [ ] Tambah field `evidence` per gejala
  - [ ] Hapus field `mb`, `md` per gejala
- [ ] Expand `symptoms.json` v2
  - [ ] Tambah `short_desc` per gejala (40 gejala)
  - [ ] Tambah `how_to_check` per gejala
  - [ ] Tambah `tutorial` object per gejala (definition, verification_steps, interpretation, common_causes, related_symptoms)
- [ ] Update `data/problems.json` jika ada perubahan kategori/deskripsi (minor)
- [ ] Tambah orphan symptoms yang di-resolve ke rule yang sesuai (kalau ada)
- [ ] **Validasi JSON schema** (pakai `jsonschema` validator):
  - [ ] Semua rule punya ≥ 2 symptoms
  - [ ] Semua gejala di rule punya `cf_pakar` di [0.1, 1.0]
  - [ ] Semua rule punya ≥ 2 `sources`
  - [ ] Semua gejala di symptoms.json punya tutorial lengkap
  - [ ] Format URL di `sources` valid
- [ ] Manual smoke test load KB di Python REPL (cek `KnowledgeBase().rules` & `.symptoms`)

---

## Phase 3 — Implementasi Inference Engine

- [ ] Baca `inference/engine.py` v1.0.0 sekali lagi sebagai baseline konfirmasi
- [ ] **Drop:**
  - [ ] Function `calculate_cf_rule(mb, md)` (line 8-10)
  - [ ] AND-strict matching `issubset` (line 36-37)
  - [ ] Top-3 truncation `results[:3]` (line 92)
  - [ ] Trace fields `mb`, `md`, `cf_rule` di evidence_steps (line 60-78)
- [ ] **Update:**
  - [ ] `calculate_cf_evidence` signature: param `cf_rule` → `cf_pakar`
  - [ ] Trace evidence_steps: tambah `cf_pakar`, `evidence_note`
  - [ ] Trace evidence_steps: tambah `percentage`, `label`, `matched_count` di result
- [ ] **Implementasi baru:**
  - [ ] Filter "≥ 2 gejala relevan dipilih user" (ganti `issubset`)
  - [ ] Method `_combine_cfs_with_trace` (refactor dari `_combine_cfs`, return trace)
  - [ ] Rename `forward_chaining()` → `diagnose()` (recommended)
- [ ] **Update `knowledge_base.py`:**
  - [ ] Handle schema baru (cf_pakar, evidence, sources)
  - [ ] Add method `get_symptom(code)` untuk route `/tutorial/<code>`
  - [ ] Add method `get_symptoms_with_info()` untuk modal info di symptoms.html

---

## Phase 4 — Implementasi Backend (app.py)

- [ ] Update clamping CF_user (line ~180):
  - [ ] Ganti `max(-1.0, min(1.0, cf_val))` → `max(0.1, min(1.0, cf_val))`
- [ ] Add route `/tutorial/<code>`:
  - [ ] Normalize code `.upper()`
  - [ ] Lookup symptom via `kb.get_symptom(code)`
  - [ ] 404 handler jika tidak ketemu
  - [ ] Resolve `related_symptoms` untuk link
  - [ ] Render `tutorial.html`
- [ ] Update diagnosis route `/diagnose`:
  - [ ] Ganti pemanggilan `engine.forward_chaining()` → `engine.diagnose()`
  - [ ] Pass `results` (ALL candidates) ke template, bukan top-3
  - [ ] Build `kesimpulan` narasi via helper `build_kesimpulan(results)`
  - [ ] Pass `kesimpulan` ke template
- [ ] Update SQLite history save:
  - [ ] Struktur kolom tetap (id, timestamp, selected_symptoms_json, results_json)
  - [ ] Results sekarang berisi field baru (percentage, label, matched_count)
  - [ ] Add migration lazy rendering flag (cek field `percentage` existence)
- [ ] Add helper `build_kesimpulan(results)` di app.py

---

## Phase 5 — Implementasi Frontend (Templates)

### 5.A symptoms.html (Step 1 — Pilih Gejala)

- [ ] Tambah info button (ⓘ) inline di samping tiap gejala
- [ ] Implementasi modal info (single modal, populated dynamically via JS):
  - [ ] Tampilkan `short_desc`
  - [ ] Tampilkan `how_to_check` (monospace block)
  - [ ] Link "Pelajari lebih lanjut →" → `/tutorial/<code>`
  - [ ] Tombol tutup
- [ ] Inject symptom data via Jinja2 → JS global `SYMPTOM_DATA`
- [ ] Styling modal (Tailwind: overlay, fixed center, max-width)
- [ ] Styling info button (subtle, tidak ganggu checkbox)
- [ ] Optional: badge "belum didukung sistem" untuk orphan symptoms

### 5.B diagnose.html (Step 2 — Pilih CF_user)

- [ ] Ganti input ke **radio button 5 level** per gejala yang sudah dipilih:
  - [ ] 0.1 — Hampir Tidak Yakin
  - [ ] 0.3 — Kurang Yakin
  - [ ] 0.5 — Cukup Yakin (default pre-checked)
  - [ ] 0.7 — Yakin
  - [ ] 1.0 — Sangat Yakin
- [ ] Layout: grid 5 kolom (responsive, stack di mobile)
- [ ] Styling radio card (selected state distinct)
- [ ] Form validation: pastikan setiap gejala yang dipilih Step 1 ada radio-nya
- [ ] JS: sinkronisasi state radio antar gejala (default 0.5 jika user belum pilih)

### 5.C result.html (Hasil Diagnosis)

- [ ] Tambah **Section Kesimpulan** di atas:
  - [ ] Empty state: tampilkan pesan "tidak ada diagnosis lolos filter"
  - [ ] Found state: narasi kandidat utama + persentase + label
  - [ ] List alternatif (maks 3 di narasi, sisanya di detail section)
- [ ] **Section Detail Kandidat** — tampil semua (bukan top-3):
  - [ ] Card per problem dengan header (code, name, percentage badge)
  - [ ] Match count indicator (matched/total symptoms in rule)
- [ ] **Section Trace Perhitungan** (collapsible per card):
  - [ ] Tabel evidence_steps dengan kolom: Symptom | CF_pakar | CF_user | CF_evidence
  - [ ] **Hapus** kolom MB, MD, CF_rule
  - [ ] Tambah evidence_note (justifikasi pakar)
  - [ ] Tabel combine_steps dengan kolom: Step | CFₐ | CFᵦ | Result
- [ ] Styling: badge label (Sangat Yakin hijau, Kurang Yakin abu, dst)
- [ ] Responsive: card stack di mobile

### 5.D tutorial.html (BARU)

- [ ] Layout format **mirip YAML frontmatter**:
  - [ ] Header card: dark background (gray-900), monospace, syntax highlighting warna
  - [ ] Body: section terpisah (Definisi, Cara Verifikasi, Interpretasi, Penyebab Umum, Gejala Terkait)
- [ ] Tombol "← Kembali ke form" di atas
- [ ] Render `verification_steps` sebagai ordered list
- [ ] Render `common_causes` sebagai unordered list
- [ ] Render `related_symptoms` sebagai link ke `/tutorial/<related_code>`
- [ ] Max-width constraint (max-w-3xl) untuk readability
- [ ] Styling konsisten dengan tema NetMedix (Tailwind + Inter font)

### 5.E CSS/Styling Updates

- [ ] Style untuk tooltip/modal di symptoms.html
- [ ] Style untuk radio button group (5 card) di diagnose.html
- [ ] Style untuk YAML-like card di tutorial.html
- [ ] Style untuk kesimpulan box di result.html
- [ ] Cek responsive di breakpoint: 375px (mobile), 768px (tablet), 1024px (desktop)

---

## Phase 6 — Integrasi & Polish

- [ ] Update admin panel (kalau ada):
  - [ ] CRUD rule dengan schema baru (cf_pakar, evidence, sources)
  - [ ] CRUD symptom dengan field tutorial (definition, verification_steps, dst)
  - [ ] Form validation sesuai schema v2
- [ ] Update halaman histori diagnosis:
  - [ ] Adaptasi format baru (ada percentage, label)
  - [ ] Lazy render untuk entry lama (v1 schema) — flag "diagnosa v1"
- [ ] Update README.md dengan breaking changes v2.0.0 + migration notes
- [ ] Update VERSION file / version constant di app.py → "2.0.0"
- [ ] **Responsive check** mobile (375px) & tablet (768px):
  - [ ] symptoms.html
  - [ ] diagnose.html
  - [ ] result.html
  - [ ] tutorial.html
- [ ] **Accessibility check:**
  - [ ] Semua input punya `<label>`
  - [ ] Modal bisa di-dismiss via keyboard (Esc)
  - [ ] Focus state jelas (focus-visible)
  - [ ] Color contrast AA (badge label, button)
- [ ] **Performance check:**
  - [ ] KB load time (< 100ms idealnya)
  - [ ] Page render time
  - [ ] Tutorial page load time

---

## Phase 7 — Testing & QA

### 7.A Unit Test Engine (Python)

Pakai script Python atau pytest. Manual calc reference dari tabel CF_pakar.

- [ ] **T1 — Single symptom P12:** Input `{G15: 0.7}` → expected: empty result (gagal filter ≥ 2)
- [ ] **T2 — Multi-symptom P15:** Input `{G19: 1.0, G27: 0.8, G34: 1.0}` → expected: P15 CF sesuai manual calc dari tabel riset
- [ ] **T3 — 1 gejala relevan saja:** Input `{G02: 0.7}` → expected: empty (P02 butuh ≥ 2)
- [ ] **T4 — 0 gejala:** Input `{}` → expected: empty result
- [ ] **T5 — Orphan gejala saja:** Input `{G31: 0.7}` → expected: empty (G31 tidak di rule manapun)
- [ ] **T6 — Cross-cutting:** Input `{G14: 0.9, G23: 0.7, G18: 0.8, G29: 0.9}` → expected: P11 (G14+G23) DAN P14 (G18+G29+G14) muncul, sort desc by CF

### 7.B E2E Test via Chrome Devtools MCP

Server Flask harus running di `localhost:5000` sebelum test.

- [ ] **E2E-1 — User flow lengkap:** Home → klik mulai → pilih gejala → next → pilih CF_user → submit → result page tampil
- [ ] **E2E-2 — Tooltip/modal info:** Di symptoms.html, klik ⓘ icon → modal tampil dengan short_desc + how_to_check + link tutorial
- [ ] **E2E-3 — Link tutorial:** Klik "Pelajari lebih lanjut" → halaman `/tutorial/<code>` tampil dengan layout YAML-like + body sections
- [ ] **E2E-4 — Skenario P02 (Internet putus):** Centang G02, G03, G28 → CF 1.0/1.0/0.8 → submit → top result P02 dengan percentage tinggi
- [ ] **E2E-5 — Skenario P05 (DHCP failure):** Centang G05, G30, G40 → CF tinggi → submit → top result P05
- [ ] **E2E-6 — Edge case < 2 gejala:** Centang hanya G02 → submit → result page tampilkan empty state (bukan error)
- [ ] **E2E-7 — Histori diagnosis:** Lakukan diagnosis → buka halaman histori → entry tampil dengan format baru
- [ ] **E2E-8 — Responsive mobile:** Resize viewport ke 375px → semua halaman tetap readable, tidak overflow horizontal

**Untuk setiap E2E:**
- [ ] Screenshot di-capture (`mcp__chrome-devtools__take_screenshot`)
- [ ] Console messages di-cek (`list_console_messages` — tidak boleh ada error)
- [ ] Network requests di-cek (`list_network_requests` — status 200 untuk assets)
- [ ] Snapshot DOM (`take_snapshot`) untuk verifikasi struktur

### 7.C Lighthouse Audit

Jalankan `mcp__chrome-devtools__lighthouse_audit` di halaman utama:

- [ ] Accessibility ≥ 90
- [ ] Best Practices ≥ 90
- [ ] (Performance ≥ 70 — nice to have, bukan blocker)

### 7.D Bug Fix Round

- [ ] Triage issue dari E2E (P0/P1/P2)
- [ ] Fix P0/P1 issue
- [ ] Re-run E2E yang gagal
- [ ] Regression test scenario v1.0.0 (optional — untuk dokumentasi perubahan behavior)

---

## Phase 8 — Deployment & Version Bump

- [ ] Update version di `app.py` (atau VERSION file jika ada): `1.0.0` → `2.0.0`
- [ ] Update README.md dengan:
  - [ ] Changelog v2.0.0 (breaking changes, new features)
  - [ ] Migration notes (kalau ada user existing)
- [ ] Final review dengan user (demo semua fitur baru)
- [ ] User acceptance test approved
- [ ] Git commit: `feat: rombak v2.0.0 — pure CF + tutorial gejala + CF_pakar riset-based`
- [ ] Git tag: `v2.0.0`
- [ ] Handover & demo untuk reviewer kuliah

---

## Progress Tracking

Update secara berkala:

| Fase | Status | Progress | Catatan |
|---|---|---|---|
| 0 — Persiapan & Perencanaan | ✅ Done | 8/8 | 3 dokumen + discussion log siap |
| 1 — Riset Knowledge Base | 🔄 In Progress | ~20/~50 (1.A done) | **1.A sample P12 & P15 selesai; metodologi Opsi D VALIDATED; G33 orphan resolved; lanjut 1.B** |
| 2 — Migrasi Data | ⏸ Pending | 0/10 | Setelah Fase 1 settle |
| 3 — Inference Engine | ⏸ Pending | 0/15 | Setelah Fase 2 |
| 4 — Backend (app.py) | ⏸ Pending | 0/8 | Setelah Fase 3 |
| 5 — Frontend (Templates) | ⏸ Pending | 0/25 | Setelah Fase 4 |
| 6 — Integrasi & Polish | ⏸ Pending | 0/15 | Setelah Fase 5 |
| 7 — Testing & QA | ⏸ Pending | 0/20 | Setelah Fase 6 |
| 8 — Deployment & Version Bump | ⏸ Pending | 0/8 | Setelah Fase 7 |

**Estimasi total task: ~160 items** (akan di-refine saat eksekusi)

---

## Notes Eksekusi

- **Urutan dependency ketat:** Phase 1 → 2 → 3 → 4 → 5. Phase 6, 7 bisa overlap dengan 5.
- **Sample dulu:** Jangan produksi massal Phase 1.B sebelum 1.A di-review user.
- **Bundling efisien:** Saat riset penyakit (Phase 1.B), sekalian isi tutorial gejala (Phase 1.E). Hemat effort baca sumber sekali.
- **E2E wajib lewat Chrome Devtools MCP** — bukan manual click. Capture screenshot untuk dokumentasi.
- **Discussion log di-update** setiap major milestone (selesai fase, temuan penting, pivot keputusan).

---

*Last update: 2026-07-09 | Owner: AI (Claude) + User | Status: Phase 1.A selesai (sample P12 & P15 validated, metodologi Opsi D PASSED); next Phase 1.B — produksi massal 13 penyakit*
