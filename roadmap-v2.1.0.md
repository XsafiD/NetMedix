---
created_at: 2026-07-16
version_target: "2.1.0"
project: "NetMedix"
topic: "Roadmap NetMedix v2.1.0 — Admin Panel Enhancement & Quality Improvements"
tags: [roadmap, v2.1.0, admin-panel, quality-of-life, enhancement]
related_files:
  - "[TODO v2.0.0](./todo-rombak-v2.0.0-NetMedix.md)"
  - "[Perencanaan v2.0.0](./perencanaan-rombak-v2.0.0-NetMedix.md)"
  - "[Desain teknis v2.0.0](./desain-teknis-v2.0.0-NetMedix.md)"
status: "backlog"
ai_model: "Claude (glm-5)"
---

# Roadmap NetMedix v2.1.0 — Admin Panel Enhancement & Quality Improvements

> **Status:** Backlog — Future iteration setelah v2.0.0 stable
> **Focus:** Admin panel CRUD untuk v2 schema, accessibility, performance, UX enhancements

---

## Executive Summary

NetMedix v2.0.0 telah **complete** untuk semua core functionality (Pure CF, tutorial gejala, kesimpulan naratif, responsive design). **v2.1.0** adalah iterasi enhancement berikutnya yang fokus pada:

1. **Admin Panel v2** — CRUD knowledge base dengan schema v2 (CF_pakar, evidence, sources, tutorial)
2. **Quality of Life** — Accessibility improvements, performance optimization
3. **UX Enhancements** — Better user experience untuk diagnosis flow

**Rationale:** Admin panel v1 masih menggunakan schema MB/MD yang deprecated. Untuk v2.0.0, developer harus edit JSON langsung. v2.1.0 akan mengembalikan convenience admin panel dengan schema v2 support.

---

## Priority Legend

| Priority | Description | Timeline |
|----------|-------------|----------|
| **P0** | Critical — breaking admin functionality | v2.1.0 Must-Have |
| **P1** | High — significant UX improvement | v2.1.0 Nice-to-Have |
| **P2** | Medium — polish & optimization | v2.1.0 Stretch |
| **P3** | Low — future enhancement | v2.2.0+ Backlog |

---

## Phase 1 — Admin Panel v2 (P0 — Critical)

### 1.A. Rules CRUD — Schema v2 Support

**Current State (v1):**
- Form menggunakan MB/MD fields
- Tidak ada field `sources` per rule
- Tidak ada field `evidence` per symptom

**Target State (v2):**
- Form menggunakan CF_pakar + Evidence fields
- Field `sources` per rule (minimal 2 URL)
- Field `evidence` per symptom (justifikasi singkat)

**Tasks:**

- [ ] **Update `templates/admin/rules.html` form:**
  - [ ] Ganti input `mb[]` → `cf_pakar[]` (range 0.1-1.0, default 0.5)
  - [ ] Hapus input `md[]`
  - [ ] Tambah input `evidence[]` (textarea, justifikasi singkat)
  - [ ] Tambah input `sources[]` (array URL, minimal 2, dengan tombol "Add Source")
  - [ ] Update form validation (minimal 2 sources, semua cf_pakar [0.1, 1.0])

- [ ] **Update `app.py` — `admin_rules_add()` (line ~593-643):**
  - [ ] Parse `symptom_cf_pakars` dari form
  - [ ] Parse `symptom_evidences` dari form
  - [ ] Parse `rule_sources` dari form
  - [ ] Validate: minimal 2 sources, semua cf_pakar dalam range [0.1, 1.0]
  - [ ] Build rule object dengan schema v2:
    ```python
    new_rule = {
        "code": code,
        "name": name,
        "target_problem": target_problem,
        "sources": sources_list,  # NEW
        "symptoms": [
            {"code": sc, "cf_pakar": cf_pakar, "evidence": evidence}
            for sc, cf_pakar, evidence in zip(...)
        ]
    }
    ```

- [ ] **Update `app.py` — `admin_rules_edit()` (line ~646-680):**
  - [ ] Sama logic seperti `admin_rules_add()`
  - [ ] Preserve existing `sources` jika user tidak mengubah

- [ ] **Update `templates/admin/rules.html` — Table display:**
  - [ ] Tampilkan column `sources` (count atau preview)
  - [ ] Tampilkan column `cf_pakar` (bukan MB/MD)
  - [ ] Tampilkan column `evidence` (truncate preview)

**Effort Estimate:** 4-6 hours

---

### 1.B. Symptoms CRUD — Tutorial Fields Support

**Current State (v1):**
- Form hanya: code, name, question, category
- Tidak ada field `short_desc`, `how_to_check`, `tutorial`

**Target State (v2):**
- Form dengan semua field v2: short_desc, how_to_check, tutorial (5 sub-fields)

**Tasks:**

- [ ] **Update `templates/admin/symptoms.html` form:**
  - [ ] Tambah input `short_desc` (textarea, 1-2 kalimat)
  - [ ] Tambah input `how_to_check` (textarea, command cepat)
  - [ ] Tambah section `tutorial` dengan 5 fields:
    - `definition` (textarea)
    - `verification_steps` (textarea, support multiline/split by newline)
    - `interpretation` (textarea, format: "X%: category | Y%: category")
    - `common_causes` (textarea, support multiline/split by newline)
    - `related_symptoms` (input tags/select multi symptom codes)
  - [ ] Update form validation (semua field required kecuali related_symptoms)

- [ ] **Update `app.py` — `admin_symptoms_add()` (line ~519-547):**
  - [ ] Parse semua fields baru dari form
  - [ ] Convert multiline string ke array untuk `verification_steps` dan `common_causes`
  - [ ] Parse `related_symptoms` (split comma/space ke array codes)
  - [ ] Build symptom object dengan schema v2:
    ```python
    new_symptom = {
        "code": code,
        "name": name,
        "question": question,
        "category": category,
        "short_desc": short_desc,
        "how_to_check": how_to_check,
        "tutorial": {
            "definition": definition,
            "verification_steps": steps_list,  # array
            "interpretation": interpretation,
            "common_causes": causes_list,       # array
            "related_symptoms": related_codes  # array
        }
    }
    ```

- [ ] **Update `app.py` — `admin_symptoms_edit()` (line ~550-565):**
  - [ ] Sama logic seperti `admin_symptoms_add()`
  - [ ] Preserve existing tutorial data jika field kosong

- [ ] **Update `templates/admin/symptoms.html` — Table display:**
  - [ ] Tampilkan column `short_desc` (truncate preview)
  - [ ] Tampilkan column `has_tutorial` (badge yes/no)

**Effort Estimate:** 6-8 hours

---

### 1.C. Problems CRUD — Minor Updates

**Current State (v1):** — Sudah cukup good, tidak ada breaking changes dari v1

**Target State (v2):** — Tetap sama, mungkin minor UX improvements

**Tasks (Optional/P2):**

- [ ] **Improve UX `templates/admin/problems.html`:**
  - [ ] Add preview/render untuk `causes` dan `solutions` (multiline arrays)
  - [ ] Add validation untuk empty lines di causes/solutions

**Effort Estimate:** 1-2 hours (optional)

---

### 1.D. Admin Panel — Form Validation v2

**Tasks:**

- [ ] **Update validation messages** untuk schema v2:
  - [ ] Error message jika cf_pakar < 0.1 atau > 1.0
  - [ ] Error message jika sources < 2 URL
  - [ ] Error message jika URL di sources tidak valid (optional)
  - [ ] Error message jika tutorial fields kosong

- [ ] **Add client-side validation (JavaScript):**
  - [ ] Real-time validation untuk cf_pakar range
  - [ ] Real-time validation untuk minimal 2 sources
  - [ ] Preview untuk verification_steps dan common_causes (split by newline)

**Effort Estimate:** 2-3 hours

---

## Phase 2 — Accessibility Improvements (P1 — High)

**Current State:** — HTML templates sudah semantic tapi belum comprehensive accessibility check

**Target State:** — WCAG 2.1 AA compliance

**Tasks:**

- [ ] **A11y Audit — Semua input punya `<label>` proper:**
  - [ ] Check semua forms (diagnose, diagnose_step2, admin panel)
  - [ ] Ensure semua input punya `for` attribute yang match dengan `id`
  - [ ] Add `aria-label` untuk icon-only buttons (ℹ️ info button, delete button, dll)

- [ ] **Keyboard Navigation:**
  - [ ] Test semua interactive elements via keyboard (Tab, Enter, Space)
  - [ ] Ensure modal bisa di-dismiss via Escape key (sudah ada di history.html, cek yang lain)
  - [ ] Add focus trap untuk modal (tab cycle dalam modal saja)
  - [ ] Ensure focus visible state jelas (`focus-visible` CSS)

- [ ] **Color Contrast:**
  - [ ] Audit semua text vs background contrast (target AA: 4.5:1 untuk normal text, 3:1 untuk large text)
  - [ ] Audit badge label colors (Sangat Yakin hijau, Kurang Yakin abu, dst) vs background
  - [ ] Fix contrast ratios yang tidak pass

- [ ] **Screen Reader Support:**
  - [ ] Add `aria-live` regions untuk dynamic content (error messages, flash messages)
  - [ ] Add `role="alert"` untuk error states
  - [ ] Ensure semantic heading hierarchy (h1 → h2 → h3, tidak skip)

**Effort Estimate:** 4-6 hours

---

## Phase 3 — Performance Optimization (P1 — High)

**Current State:** — Performance acceptable tapi belum measured/optimized

**Target State:** — < 100ms KB load, < 2s page render (ideal)

**Tasks:**

- [ ] **KB Load Time Measurement:**
  - [ ] Add timing measurement untuk `KnowledgeBase.__init__()`
  - [ ] Target: < 100ms untuk load semua JSON (rules, symptoms, problems)
  - [ ] Jika > 100ms, consider caching atau lazy loading

- [ ] **Page Render Time Measurement:**
  - [ ] Add client-side timing untuk setiap page load (`performance.now()`)
  - [ ] Measure: symptoms.html, diagnose_step2.html, result.html, tutorial.html
  - [ ] Target: < 2s untuk first paint, < 3s untuk fully loaded

- [ ] **Tutorial Page Load Optimization:**
  - [ ] Tutorial page load heaviest karena banyak text content
  - [ ] Consider: lazy load tutorial content atau pagination untuk long tutorials
  - [ ] Measure current load time, optimize jika > 3s

- [ ] **Database Query Optimization (SQLite):**
  - [ ] Add index ke `history.created_at` jika sering query sort by date
  - [ ] Check query time untuk `get_all_sessions()` dengan 100+ entries

**Effort Estimate:** 3-4 hours

---

## Phase 4 — UX Enhancements (P1 — High)

**Tasks:**

- [ ] **Diagnosis Flow — Progress Indicator:**
  - [ ] Add progress bar/steps indicator: "Step 1/3: Pilih Gejala" → "Step 2/3: Keyakinan" → "Step 3/3: Hasil"
  - [ ] Visual feedback untuk current step

- [ ] **Symptoms Selection — Quick Select:**
  - [ ] Add "Select All" button per category
  - [ ] Add "Clear All" button per category
  - [ ] Add symptom count indicator: "5 gejala dipilih"

- [ ] **Result Page — Export/Share:**
  - [ ] Add "Copy Summary" button (copy kesimpulan naratif ke clipboard)
  - [ ] Add "Print/Export PDF" button untuk hasil diagnosis
  - [ ] Add "Share Link" button (generate URL dengan session ID)

- [ ] **History Page — Search/Filter:**
  - [ ] Add search box untuk filter by problem name
  - [ ] Add date range filter
  - [ ] Add sort options (newest, oldest, highest CF)

**Effort Estimate:** 4-5 hours

---

## Phase 5 — Polish & Bug Fixes (P2 — Medium)

**Tasks:**

- [ ] **Error Handling Improvements:**
  - [ ] Better error page untuk 404 (tutorial not found)
  - [ ] Better error message untuk invalid symptom codes
  - [ ] Add user-friendly error message untuk JSON parse errors (KB corruption)

- [ ] **Loading States:**
  - [ ] Add loading spinner untuk diagnosis process (jika > 1s)
  - [ ] Add skeleton loading untuk tutorial page (jika lazy load)

- [ ] **Mobile UX Polish:**
  - [ ] Check semua tappable elements ≥ 44x44px (iOS HIG)
  - [ ] Check text input tidak zoom on focus (font-size ≥ 16px)
  - [ ] Check horizontal overflow tidak terjadi di manapun

- [ ] **Bug Fixes — Reported from v2.0.0:**
  - [ ] (Placeholder) — collect bugs from v2.0.0 usage

**Effort Estimate:** 2-3 hours

---

## Phase 6 — Testing & Documentation (P1 — High)

**Tasks:**

- [ ] **E2E Test Coverage Expansion:**
  - [ ] Add E2E test untuk admin panel CRUD flows
  - [ ] Add E2E test untuk accessibility (keyboard navigation)
  - [ ] Add E2E test untuk mobile viewport (375px)

- [ ] **Unit Test Coverage:**
  - [ ] Add unit test untuk admin panel form validation
  - [ ] Add unit test untuk JSON schema validation (rules.json, symptoms.json)
  - [ ] Target: ≥ 80% coverage untuk critical paths

- [ ] **Documentation Updates:**
  - [ ] Update README.md untuk v2.1.0 features
  - [ ] Update admin panel documentation (how-to use v2 schema)
  - [ ] Add developer guide untuk menambah symptom baru dengan tutorial

**Effort Estimate:** 3-4 hours

---

## Dependencies & Blockers

| Phase | Dependency | Blocker |
|-------|-----------|---------|
| Phase 1 (Admin Panel v2) | v2.0.0 stable | None — JSON edit workaround exists |
| Phase 2 (A11y) | v2.0.0 stable | None — independent |
| Phase 3 (Performance) | v2.0.0 stable | None — independent |
| Phase 4 (UX Enhancements) | v2.0.0 stable | None — independent |
| Phase 5 (Polish) | Phase 4 complete | None — can parallel |
| Phase 6 (Testing) | Phase 1-5 complete | Need features to test first |

**Parallelizable:** Phase 2, 3, 4 can be done in parallel. Phase 5 dependent on Phase 4. Phase 6 dependent on Phase 1-5.

---

## Timeline Estimate

| Phase | Effort | Priority | Target Release |
|-------|--------|----------|----------------|
| Phase 1 — Admin Panel v2 | 13-19 hours | P0 | v2.1.0 Must-Have |
| Phase 2 — Accessibility | 4-6 hours | P1 | v2.1.0 Nice-to-Have |
| Phase 3 — Performance | 3-4 hours | P1 | v2.1.0 Nice-to-Have |
| Phase 4 — UX Enhancements | 4-5 hours | P1 | v2.1.0 Nice-to-Have |
| Phase 5 — Polish | 2-3 hours | P2 | v2.1.0 Stretch |
| Phase 6 — Testing | 3-4 hours | P1 | v2.1.0 Nice-to-Have |
| **Total** | **29-41 hours** | | **~1-1.5 weeks**** |

**Conservative Estimate:** 2 weeks (dengan testing & buffer)

---

## Milestones

### Milestone 1 — Admin Panel v2 Complete (P0)
- [ ] Rules CRUD v2 functional
- [ ] Symptoms CRUD v2 functional
- [ ] Form validation v2 complete
- [ ] Smoked test: add → edit → delete rule/symptom via admin panel

### Milestone 2 — Quality Improvements Complete (P1)
- [ ] Accessibility audit pass (WCAG 2.1 AA)
- [ ] Performance targets met (< 100ms KB load, < 2s page render)
- [ ] UX enhancements implemented (progress indicator, quick select, export)

### Milestone 3 — v2.1.0 Release Candidate
- [ ] All P0 & P1 tasks complete
- [ ] E2E test pass (admin flow + accessibility + mobile)
- [ ] Documentation updated
- [ ] Ready for beta testing

---

## Open Questions

1. **Admin Panel vs JSON Edit Priority** — Apakah admin panel v2 benar-benar needed atau JSON edit cukup?
   - **Recommendation:** Admin panel v2 needed untuk usability, JSON edit hanya fallback

2. **Accessibility Standard** — Target WCAG level? AA atau AAA?
   - **Recommendation:** WCAG 2.1 AA (reasonable effort, good coverage)

3. **Performance Baseline** — Apakah target < 100ms KB load terlalu aggressive?
   - **Recommendation:** Measure current baseline dulu, set target realistic

4. **Timeline v2.1.0** — Kapan target release v2.1.0?
   - **Recommendation:** Setelah v2.0.0 stable + user feedback, ~1-2 bulan

5. **Backward Compatibility** — Apakah perlu maintain admin panel v1 parallel dengan v2?
   - **Recommendation:** Tidak, replace v1 dengan v2 (breaking change acceptable untuk minor version bump)

---

## Notes for Developer

### Starting Point for v2.1.0 Development

1. **Branch from:** `master` setelah v2.0.0 tag stable
2. **Create branch:** `feature/v2.1.0-admin-panel`
3. **First task:** Phase 1.A — Rules CRUD v2 (highest impact)

### Key Files to Modify

**Admin Panel v2:**
- `app.py` (lines ~193-691 — admin CRUD functions)
- `templates/admin/rules.html` (form + table)
- `templates/admin/symptoms.html` (form + table)

**Accessibility:**
- All templates (add proper labels, ARIA attributes)
- `static/css/` (add focus-visible styles)

**Performance:**
- `inference/knowledge_base.py` (add timing measurements)
- All templates (add client-side timing)

### Testing Strategy

1. **Manual testing** admin panel CRUD untuk setiap change
2. **E2E test** via Chrome DevTools MCP untuk critical flows
3. **Accessibility audit** menggunakan axe DevTools atau Lighthouse
4. **Performance measurement** menggunakan Chrome DevTools Performance tab

### Rollback Plan

Jika v2.1.0 introduces breaking bugs:
1. Revert to `v2.0.0` tag
2. Hotfix fixes pada branch `hotfix/v2.1.0-x`
3. Release `v2.1.1` dengan fixes

---

*Last updated: 2026-07-16 | Status: Backlog | Next Review: Setelah v2.0.0 stable + user feedback*
