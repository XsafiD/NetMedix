---
created_at: 2026-07-09
version_target: 2.0.0
project: NetMedix
topic: Perencanaan Rombak Major NetMedix v1.0.0 → v2.0.0
tags:
  - expert-system
  - certainty-factor
  - netmedix
  - rombak
  - perencanaan
  - major-version
related_files:
  - "[Discussion log](../../00_INBOX/2026-07-09_discussion-rombak-netmedix-pure-cf.md)"
  - "[Desain teknis](./desain-teknis-v2.0.0-NetMedix.md)"
  - "[TODO tasklist](./todo-rombak-v2.0.0-NetMedix.md)"
  - "[Analisis baseline v1.0.0](analisis-cf-forward-chaining-v1.0.0-NetMedix.md)"
  - "[Tabel KB v1.0.0](./docs-NetMedix/2026-07-06_analisis-cf-forward-chaining-netmedix.md)"
status: planning
ai_model: Claude (glm-5)
---

# Perencanaan Rombak Major NetMedix v1.0.0 → v2.0.0

> Dokumen perencanaan tingkat tinggi (PRD-style) untuk perombakan major NetMedix. Menjawab **APA dan KENAPA**, bukan BAGAIMANA (lihat `desain-teknis-v2.0.0-NetMedix.md`).

---

## Executive Summary

NetMedix v2.0.0 adalah perombakan major yang mengubah paradigma sistem pakar dari **hybrid Forward Chaining AND-strict + Certainty Factor (MB-MD)** menjadi **Pure Certainty Factor dengan CF_pakar langsung dari riset multi-source**. Rombak ini juga menambahkan layer UX tutorial gejala inline untuk meningkatkan akurasi input user awam.

Versi 2.0.0 **bukan** patch incremental — mengubah fundamental: schema knowledge base, formula inference, range input user, dan struktur output.

---

## 1. Justifikasi Major Bump (v2.0.0)

Rombak ini diklasifikasikan **major** (bukan minor/patch) karena breaking changes di 4 area:

### A. Breaking Changes pada Schema Data
- `rules.json` schema berubah total: hapus field `mb`/`md`, tambah field `cf_pakar`/`evidence`/`sources`
- `symptoms.json` schema berubah: tambah field `short_desc`/`how_to_check`/`tutorial`
- Histori diagnosis lama (SQLite, struktur v1) tidak kompatibel tanpa migrasi/fallback

### B. Breaking Changes pada Behavior
- Filter inference: AND-strict (semua gejala harus ada) → partial match (≥ 2 gejala relevan)
- Output: top-3 diagnosis → semua kandidat yang lolos filter
- Range CF_user: [-1, 1] → [0.1, 1.0]

### C. Breaking Changes pada API/UI
- Route baru `/tutorial/<code>` (tidak ada di v1)
- UI form input CF_user: free input → radio button 5 level
- Hasil diagnosis: tambah narasi kesimpulan

### D. Breaking Changes pada Formula
- Hapus rumus `CF_rule = MB − MD` (1 dari 3 rumus inti v1)
- Sisa 2 rumus CF bekerja dengan asumsi baru (CF_user selalu positif, MD dihapus)

### Versi Alternatif yang Ditolak

| Opsi | Alasan ditolak |
|---|---|
| v1.1.0 (minor) | Tidak sesuai — ada breaking schema changes (semantik versi) |
| v1.0.1 (patch) | Bukan bug fix, ada perubahan fitur besar |
| v3.0.0 | Overkill — tidak ada rewrite arsitektur dari nol, foundation Flask/JSON/KB tetap |

---

## 2. Tujuan & Scope

### Tujuan Utama
1. **Meningkatkan akurasi epistemologis** — nilai keyakinan pakar diturunkan dari riset multi-source, bukan angka ngarang MB/MD
2. **Meningkatkan coverage diagnosis** — drop AND-strict matching agar diagnosis tetap muncul meski gejala user tidak lengkap
3. **Meningkatkan usability** — tambah tutorial inline agar user awam paham gejala teknis sebelum centang
4. **Meningkatkan transparansi output** — tampil semua kandidat dengan persentase mentah × 100, plus kesimpulan naratif

### In-Scope
- Riset & produksi tabel CF_pakar untuk 15 penyakit (36+ pasangan gejala)
- Riset konten tutorial inline untuk 40 gejala (33 terpakai + 7 orphan)
- Redesign inference engine (drop forward chaining AND-strict, pure CF)
- Redesign UI form & result page
- New tutorial page per gejala
- Testing E2E via Chrome Devtools MCP

### Out-of-Scope (Non-Goals)
- Mengubah stack teknologi (Flask, SQLite, Tailwind, JSON tetap)
- Menambah problem baru di luar 15 existing (P01-P15)
- Authentication/authorization user
- Localization/Internasionalization (Bahasa Indonesia only)
- Mobile native app (web app tetap)
- AI/ML-based diagnosis (CF rule-based tetap)
- Performance optimization untuk high-traffic production
- Kompatibilitas backward ke v1.0.0 (cukup fallback lazy rendering untuk histori)

---

## 3. Breaking Changes Summary

| Area | v1.0.0 | v2.0.0 |
|---|---|---|
| Inference logic | Forward Chaining AND-strict + CF | Pure CF dengan filter "≥ 2 gejala relevan" |
| CF formula count | 3 rumus (CF_rule, CF_evidence, CF_combine) | 2 rumus (CF_evidence, CF_combine) |
| CF pakar value | Diderivasi dari MB − MD | Langsung dari riset multi-source (Opsi D) |
| rules.json schema | `{mb, md}` per gejala | `{cf_pakar, evidence}` per gejala + `sources` per rule |
| symptoms.json schema | `{code, name, category}` | + `{short_desc, how_to_check, tutorial}` |
| Range CF_user | [-1, 1] | [0.1, 1.0] |
| UI input CF_user | Free input / select | Radio button 5 level |
| Output diagnosis | Top-3 | Semua kandidat yang lolos filter |
| Tutorial gejala | Tidak ada | Tooltip inline + halaman tutorial per gejala |
| Histori SQLite | v1 schema | Fallback lazy render |

---

## 4. Stakeholders & Roles

| Pihak | Role | Kontribusi |
|---|---|---|
| User (kamu) | Product owner, SME jaringan | Spec, validasi konten CF_pakar, acceptance |
| AI (Claude) | Engineer, riset, QA | Riset, implementasi, testing |
| Reviewer kuliah | Evaluator | Laporan akhir, demo |

---

## 5. Fase Eksekusi (High-Level Overview)

Detail task per fase di `todo-rombak-v2.0.0-NetMedix.md`.

| Fase | Deskripsi | Output Utama |
|---|---|---|
| 0 | Persiapan & perencanaan dokumen | 3 dokumen (PRD, design, TODO) + discussion log |
| 1 | Riset knowledge base (CF_pakar + tutorial) | `tabel-cf-pakar-riset.md` lengkap |
| 2 | Migrasi data | `rules.json` & `symptoms.json` v2 |
| 3 | Implementasi inference engine | `engine.py` & `knowledge_base.py` v2 |
| 4 | Implementasi backend | `app.py` dengan route `/tutorial/<code>` |
| 5 | Implementasi frontend | 4 template (symptoms, diagnose, result, tutorial) |
| 6 | Integrasi & polish | Admin panel, responsive, accessibility |
| 7 | Testing & QA | Unit test engine + E2E Chrome Devtools |
| 8 | Deployment & version bump | Git tag `v2.0.0` |

---

## 6. Deliverables

### Dokumen (3 file di root project)
1. `perencanaan-rombak-v2.0.0-NetMedix.md` — file ini
2. `desain-teknis-v2.0.0-NetMedix.md` — spec teknis implementasi
3. `todo-rombak-v2.0.0-NetMedix.md` — tasklist terperinci

### Dokumen Pendukung (di `docs-NetMedix/`)
4. `tabel-cf-pakar-riset.md` — primary source of truth CF_pakar (akan dibuat Phase 1)

### Data
5. `data/rules.json` (v2 schema)
6. `data/symptoms.json` (v2 schema)
7. `data/problems.json` (update minor jika perlu)

### Kode
8. `inference/engine.py` (redesain)
9. `inference/knowledge_base.py` (adaptasi schema baru)
10. `app.py` (route baru, clamping update)
11. `templates/symptoms.html` (tooltip, link tutorial)
12. `templates/diagnose.html` (radio 5 level)
13. `templates/result.html` (kesimpulan, tampil semua)
14. `templates/tutorial.html` (BARU)

### Testing
15. Unit test engine (6 skenario)
16. E2E test via Chrome Devtools MCP (8 skenario)

---

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Konten CF_pakar tidak konsisten antar penyakit | Sedang | Sedang | Peer review silang, template strict |
| Sumber riset kurang (target ≥ 2 sumber per gejala) | Sedang | Tinggi | Allow override dengan catatan "domain knowledge", atau turunkan nilai maksimal ke 0.5 |
| Tutorial terlalu panjang → overload UI | Rendah | Sedang | Format YAML frontmatter, scannable, modular dari JSON |
| Histori lama SQLite tidak kompatibel | Tinggi | Rendah | Fallback rendering lazy / flag "diagnosa v1" |
| Engine rusak test scenario v1.0.0 | Sedang | Tinggi | Re-run test scenarios v1 di Phase 7, adjust ekspektasi |
| Tutorial page bloat (40 halaman statis) | Sedang | Rendah | Single template reusable, konten dari JSON bukan hardcoded |
| Riset terlalu lama → delay implementasi | Tinggi | Sedang | Sample 2 penyakit dulu untuk validate, baru produksi massal |
| User bingung dengan banyaknya kandidat (semua tampil) | Sedang | Rendah | Kesimpulan naratif di atas jadi prioritas, kandidat lain di section detail |

---

## 8. Acceptance Criteria (Definition of Done)

Rombak v2.0.0 dianggap selesai ketika:

- [ ] Semua deliverables (dokumen, data, kode, testing) dibuat/diupdate
- [ ] Knowledge base v2 schema terisi lengkap (15 penyakit, 40 gejala dengan tutorial)
- [ ] Engine lulus 6 unit test dengan CF sesuai manual calc
- [ ] E2E test 8 skenario lulus via Chrome Devtools MCP
- [ ] Tidak ada console error/warning di halaman utama flow
- [ ] User acceptance test (kamu) approved
- [ ] Dokumentasi (PRD, design, TODO, analisis) konsisten & up-to-date
- [ ] Git tagged `v2.0.0`

---

*Status: planning | Next: lanjut ke Fase 1.A — riset sample P12 & P15 untuk validasi metodologi Opsi D*
