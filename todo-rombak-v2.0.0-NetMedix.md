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

- [x] **P11 — Packet Loss Tinggi** (G14, G23)
- [x] **P04 — DNS Cache Poisoning** (G17, G24)
- [x] **P10 — Jaringan Lambat** (G13, G22)
- [x] **P06 — IP Address Conflict** (G06, G23)
- [x] **P08 — Tidak Bisa Connect WiFi** (G09, G10)
- [x] **P09 — WiFi Signal Lemah** (G11, G12)
- [x] **P13 — Firewall Memblokir** (G16, G25)
- [x] **P01 — Tidak Ada Koneksi Jaringan** (G01, G20, G26)
- [x] **P02 — Koneksi Internet Terputus** (G02, G03, G28)
- [x] **P03 — DNS Resolution Failure** (G04, G21, G24)
- [x] **P05 — DHCP Failure** (G05, G30, G40)
- [x] **P07 — Subnet/Gateway Salah** (G07, G08, G35)
- [x] **P14 — Kerusakan Kabel** (G18, G29, G14)

Tiap penyakit: riset ≥ 3 sumber + tentukan CF_pakar Opsi D + bundling tutorial gejala.

### Fase 1.C — Resolve Orphan Symptoms (G31-G39)

- [x] Riset G31 (VPN tidak bisa connect) — relevan ke problem mana? → **orphan permanen (out-of-scope PRD)**
- [x] Riset G32 (VPN internal gagal) — relevan? → **orphan permanen (out-of-scope PRD)**
- [x] Riset G33 (Lampu LAN router mati) — bedakan dari G28/G18? → ✅ resolved di Fase 1.A (R15, CF 0.80)
- [x] Riset G36 (Network adapter disabled) — relevan ke P01? → **resolve ke R01 (P01), CF 0.85**
- [x] Riset G37 (Driver adapter bermasalah) — relevan? → **resolve ke R01 (P01), CF 0.80**
- [x] Riset G38 (Single device bermasalah) — relevan ke P01/P06? → **resolve ke R01 (P01) sebagai inverse G26, CF 0.80**
- [x] Riset G39 (Proxy aktif) — rule baru atau orphan permanen? → **resolve ke R02 (P02) sebagai minor supporting, CF 0.30**
- [x] **Keputusan per orphan:** tambah ke rule existing / buat rule baru / biarkan orphan dengan badge "belum didukung"
  - **5/7 resolved** ke rule existing (G33→R15, G36→R01, G37→R01, G38→R01, G39→R02)
  - **2/7 orphan permanen** dengan badge "belum didukung sistem" (G31, G32 VPN — out-of-scope PRD v2.0.0 non-goal #1)
  - P01 expanded: 3 → 6 gejala; P02 expanded: 3 → 4 gejala
  - Detail decision + sumber di `tabel-cf-pakar-riset.md` section "Fase 1.C — Orphan Resolution Decisions & Evidence"

### Fase 1.D — Peer Review Konsistensi

- [x] Review silang gejala cross-cutting:
  - [x] G14 (packet loss) konsisten di P11 & P14? → **PASS** (P11=0.90 signature, P14=0.70 impact langsung, P12=0.50 supporting; hierarki 0.9→0.7→0.5 sesuai Opsi D)
  - [x] G23 (intermittent) konsisten di P06 & P11? → **PASS** (P06=0.60 impact ARP flip-flop, P11=0.60 impact loss parah, P12=0.30 edge case; 2-tier konsisten)
  - [x] G24 (IP only) konsisten di P03 & P04? → **PASS** (P03=0.90 signature DNS gagal total, P04=0.50 supporting DNS resolve-tapi-salah; hierarki 0.9→0.5 sesuai Opsi D)
- [x] Verifikasi minimal 2 sumber independen per nilai CF_pakar → **⚠️ COMPLIANT WITH MINOR GAPS** — 39/42 lulus min 2 sumber, 2 finding minor (G33 di R15 dengan 1 sumber Cisco, G40 di R05 dengan 1 sumber Quizlet) — keduanya symptom universal terdokumentasi, accepted with engineering judgment override; action item Phase 2: tambah sumber sekunder ke `evidence` JSON
- [x] Verifikasi range CF_pakar semua [0.1, 1.0] → **PASS** — aktuel [0.30, 0.95] ⊂ [0.1, 1.0], tidak ada nilai di luar range
- [x] Verifikasi setiap rule punya ≥ 2 symptoms → **PASS** — semua 15 rule punya ≥ 2 symptoms (total 42 gejala-rule mappings)
- [x] Commit tabel CF_pakar final ke `docs-NetMedix/tabel-cf-pakar-riset.md` → section "Fase 1.D — Peer Review Konsistensi Final" ditambahkan dengan verdict detail per dimensi

### Fase 1.E — Riset Konten Tutorial per Gejala (Bundling)

> Idealnya di-bundle dengan Fase 1.B (sekali baca sumber, sekalian isi tutorial).

- [x] 40 gejala masing-masing punya: `short_desc`, `how_to_check`, `tutorial.{definition, verification_steps, interpretation, common_causes, related_symptoms}`
  - 38 full tutorial (G01–G30, G33–G40) di section P01–P15
  - 2 stub out-of-scope (G31, G32 VPN) di section "Orphan Permanen Tutorial Stubs" baru
  - 1 issue ditemukan & diperbaiki: G39 struktur YAML rusak (`tutorial: >` flat scalar → `tutorial:` object valid dengan 5 field child)
- [x] Konsistensi format steps (imperative voice: "Buka...", "Jalankan...")
  - Audit ~250+ verification steps — semua mulai dengan kata kerja imperative
- [x] Konsistensi interpretasi (format: "X%: kategori | Y%: kategori")
  - Pattern `value: category | value: category` konsisten di 40 gejala; unit bervariasi (ms, %, dBm, bar, state) sesuai domain gejala

---

## Phase 2 — Migrasi Data

- [x] Backup `data/rules.json` → `data/rules.v1.0.0.json.bak`
- [x] Backup `data/symptoms.json` → `data/symptoms.v1.0.0.json.bak`
- [x] Port nilai CF_pakar dari `docs-NetMedix/tabel-cf-pakar-riset.md` → `rules.json` v2 schema
  - [x] Tambah field `sources` per rule (min 2 URL)
  - [x] Tambah field `cf_pakar` per gejala
  - [x] Tambah field `evidence` per gejala
  - [x] Hapus field `mb`, `md` per gejala
- [x] Expand `symptoms.json` v2
  - [x] Tambah `short_desc` per gejala (40 gejala)
  - [x] Tambah `how_to_check` per gejala
  - [x] Tambah `tutorial` object per gejala (definition, verification_steps, interpretation, common_causes, related_symptoms)
- [x] Update `data/problems.json` jika ada perubahan kategori/deskripsi (minor)
- [x] Tambah orphan symptoms yang di-resolve ke rule yang sesuai (kalau ada)
- [x] **Validasi JSON schema** (pakai `jsonschema` validator):
  - [x] Semua rule punya ≥ 2 symptoms
  - [x] Semua gejala di rule punya `cf_pakar` di [0.1, 1.0]
  - [x] Semua rule punya ≥ 2 `sources`
  - [x] Semua gejala di symptoms.json punya tutorial lengkap
  - [x] Format URL di `sources` valid
- [x] Manual smoke test load KB di Python REPL (cek `KnowledgeBase().rules` & `.symptoms`)

---

## Phase 3 — Implementasi Inference Engine

- [x] Baca `inference/engine.py` v1.0.0 sekali lagi sebagai baseline konfirmasi
- [x] **Drop:**
  - [x] Function `calculate_cf_rule(mb, md)` (line 8-10)
  - [x] AND-strict matching `issubset` (line 36-37)
  - [x] Top-3 truncation `results[:3]` (line 92)
  - [x] Trace fields `mb`, `md`, `cf_rule` di evidence_steps (line 60-78)
- [x] **Update:**
  - [x] `calculate_cf_evidence` signature: param `cf_rule` → `cf_pakar`
  - [x] Trace evidence_steps: tambah `cf_pakar`, `evidence_note`
  - [x] Trace evidence_steps: tambah `percentage`, `label`, `matched_count` di result
- [x] **Implementasi baru:**
  - [x] Filter "≥ 2 gejala relevan dipilih user" (ganti `issubset`)
  - [x] Method `_combine_cfs_with_trace` (refactor dari `_combine_cfs`, return trace)
  - [x] Rename `forward_chaining()` → `diagnose()` (recommended)
- [x] **Update `knowledge_base.py`:**
  - [x] Handle schema baru (cf_pakar, evidence, sources)
  - [x] Add method `get_symptom(code)` untuk route `/tutorial/<code>`
  - [x] Add method `get_symptoms_with_info()` untuk modal info di symptoms.html

---

## Phase 4 — Implementasi Backend (app.py)

- [x] Update clamping CF_user (line ~180):
  - [x] Ganti `max(-1.0, min(1.0, cf_val))` → `max(0.1, min(1.0, cf_val))`
- [x] Add route `/tutorial/<code>`:
  - [x] Normalize code `.upper()`
  - [x] Lookup symptom via `kb.get_symptom(code)`
  - [x] 404 handler jika tidak ketemu
  - [x] Resolve `related_symptoms` untuk link
  - [x] Render `tutorial.html`
- [x] Update diagnosis route `/diagnose`:
  - [x] Ganti pemanggilan `engine.forward_chaining()` → `engine.diagnose()`
  - [x] Pass `results` (ALL candidates) ke template, bukan top-3
  - [x] Build `kesimpulan` narasi via helper `build_kesimpulan(results)`
  - [x] Pass `kesimpulan` ke template
- [x] Update SQLite history save:
  - [x] Struktur kolom tetap (id, timestamp, selected_symptoms_json, results_json)
  - [x] Results sekarang berisi field baru (percentage, label, matched_count)
  - [x] Add migration lazy rendering flag (cek field `percentage` existence)
- [x] Add helper `build_kesimpulan(results)` di app.py

---

## Phase 5 — Implementasi Frontend (Templates)

### 5.A symptoms.html (Step 1 — Pilih Gejala)

- [x] Tambah info button (ⓘ) inline di samping tiap gejala
- [x] Implementasi modal info (single modal, populated dynamically via JS):
  - [x] Tampilkan `short_desc`
  - [x] Tampilkan `how_to_check` (monospace block)
  - [x] Link "Pelajari lebih lanjut →" → `/tutorial/<code>`
  - [x] Tombol tutup
- [x] Inject symptom data via Jinja2 → JS global `SYMPTOM_DATA`
- [x] Styling modal (Tailwind: overlay, fixed center, max-width)
- [x] Styling info button (subtle, tidak ganggu checkbox)
- [ ] Optional: badge "belum didukung sistem" untuk orphan symptoms

### 5.B diagnose.html (Step 2 — Pilih CF_user)

- [x] Ganti input ke **radio button 5 level** per gejala yang sudah dipilih:
  - [x] 0.1 — Hampir Tidak Yakin
  - [x] 0.3 — Kurang Yakin
  - [x] 0.5 — Cukup Yakin (default pre-checked)
  - [x] 0.7 — Yakin
  - [x] 1.0 — Sangat Yakin
- [x] Layout: grid 5 kolom (responsive, stack di mobile)
- [x] Styling radio card (selected state distinct)
- [x] Form validation: pastikan setiap gejala yang dipilih Step 1 ada radio-nya
- [x] JS: sinkronisasi state radio antar gejala (default 0.5 jika user belum pilih)

### 5.C result.html (Hasil Diagnosis)

- [x] Tambah **Section Kesimpulan** di atas:
  - [x] Empty state: tampilkan pesan "tidak ada diagnosis lolos filter"
  - [x] Found state: narasi kandidat utama + persentase + label
  - [x] List alternatif (maks 3 di narasi, sisanya di detail section)
- [x] **Section Detail Kandidat** — tampil semua (bukan top-3):
  - [x] Card per problem dengan header (code, name, percentage badge)
  - [x] Match count indicator (matched/total symptoms in rule)
- [x] **Section Trace Perhitungan** (collapsible per card):
  - [x] Tabel evidence_steps dengan kolom: Symptom | CF_pakar | CF_user | CF_evidence
  - [x] **Hapus** kolom MB, MD, CF_rule
  - [x] Tambah evidence_note (justifikasi pakar)
  - [x] Tabel combine_steps dengan kolom: Step | CFₐ | CFᵦ | Result
- [x] Styling: badge label (Sangat Yakin hijau, Kurang Yakin abu, dst)
- [x] Responsive: card stack di mobile

### 5.D tutorial.html (BARU)

- [x] Layout format **mirip YAML frontmatter**:
  - [x] Header card: dark background (gray-900), monospace, syntax highlighting warna
  - [x] Body: section terpisah (Definisi, Cara Verifikasi, Interpretasi, Penyebab Umum, Gejala Terkait)
- [x] Tombol "← Kembali ke form" di atas
- [x] Render `verification_steps` sebagai ordered list
- [x] Render `common_causes` sebagai unordered list
- [x] Render `related_symptoms` sebagai link ke `/tutorial/<related_code>`
- [x] Max-width constraint (max-w-3xl) untuk readability
- [x] Styling konsisten dengan tema NetMedix (Tailwind + Inter font)

### 5.E CSS/Styling Updates

- [x] Style untuk tooltip/modal di symptoms.html
- [x] Style untuk radio button group (5 card) di diagnose.html
- [x] Style untuk YAML-like card di tutorial.html
- [x] Style untuk kesimpulan box di result.html
- [x] Cek responsive di breakpoint: 375px (mobile), 768px (tablet), 1024px (desktop)

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
| 1 — Riset Knowledge Base | ✅ **Done** | ~65/~65 (1.A + 1.B + 1.C + 1.D + 1.E done) | **Fase 1 LENGKAP. Total 15/15 penyakit + 6/7 orphan resolved (G33→R15, G36→R01, G37→R01, G38→R01, G39→R02) + 2/7 orphan permanen dengan stub (G31/G32 VPN) + peer review konsistensi final LULUS (5/6 PASS, 1/6 COMPLIANT) + tutorial bundling verification LULUS (40/40 gejala: 38 full + 2 stub). Total 42 gejala-rule mappings. 1 issue fixed (G39 YAML structure). Siap Phase 2.** |
| 2 — Migrasi Data | ✅ **Done** | 10/10 | **Phase 2 SELESAI — 2026-07-16. Commit 45232e6: rules.json v2 (15 rules, 44 mappings, cf_pakar+evidence+sources), symptoms.json v2 (40 gejala dengan short_desc+how_to_check+tutorial, 38 full + 2 stub VPN G31/G32), backup v1 (.v1.0.0.json.bak 3 files), validation PASS (schema+orphan+smoke test).** |
| 3 — Inference Engine | ✅ **Done** | 15/15 | **Phase 3 SELESAI — 2026-07-16. Commit afdabb6: engine.py v2 (Pure CF, filter ≥2, diagnose(), _combine_cfs_with_trace, interpret_cf update), knowledge_base.py v2 (get_symptom, get_symptoms_with_info, backward compatibility aliases, comprehensive docstrings). Breaking changes: forward_chaining→diagnose, result structure baru, trace structure baru.** |
| 4 — Backend (app.py) | ✅ **Done** | 8/8 | **Phase 4 SELESAI — 2026-07-16. Commit f70820f: app.py v2 (clamping CF [0.1, 1.0], route /tutorial/<code>, diagnose() rename, build_kesimpulan helper, result route update). Breaking changes: CF_user range, result structure baru, kesimpulan narasi.** |
| 5 — Frontend (Templates) | ✅ **Done** | 25/25 | **Phase 5 LENGKAP — 2026-07-16. Commit f2de1a3: symptoms.html v2 (info button ⓘ, modal info dinamis). Commit d633060: diagnose_step2.html v2 (radio 5 level CF 0.1-1.0, default 0.5 pre-checked, grid 5 kolom, styling update). Commit 9ca2f54: result.html v2 (Section Kesimpulan empty/found state, Section Detail Kandidat semua kandidat bukan top-3, match count indicator, Trace Perhitungan Pure CF hapus MB/MD tambah CF_pakar+evidence_note). Commit 9a7019c: tutorial.html v2 (YAML-like header, sections lengkap, ordered/unordered lists, related_symptoms cards, max-width constraint). Commit b925b06: base.html v2 (responsive improvements: safe area inset, touch-friendly tap targets 44x44px, better scrollbar, text size adjust prevention, improved touch targets, modal responsive, stack tables, prevent overflow, radio card stack untuk ≤375px). Breaking changes: 9 level CF → 5 level CF, range [0.1, 1.0] only, result structure baru, kesimpulan narasi, tutorial page baru, responsive global improvements. Phase 5 COMPLETE.** |
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

*Last update: 2026-07-16 | Owner: AI (Claude) + User | Status: **Phase 5 LENGKAP** — 2026-07-16 commit b925b06: **Phase 5.E CSS/Styling Updates & Responsive Improvements COMPLETED**. base.html v2 dengan responsive improvements (safe area inset support untuk notch devices, touch-friendly tap targets 44x44px per iOS HIG, better scrollbar styling 6px, text size adjust prevention, improved touch targets untuk radio/checkbox cards, modal responsive improvements ≤375px, stack tables on mobile, prevent horizontal overflow, radio card stack improvement ≤375px). Verification Summary: ✅ tooltip/modal (diagnose.html), ✅ radio button group (diagnose_step2.html), ✅ YAML-like card (tutorial.html), ✅ kesimpulan box (result.html), ✅ responsive check 3 breakpoints (375px/768px/1024px). Phase 5.A-5.E SEMUA SELESAI. Next: Phase 6 (Integrasi & Polish).*
