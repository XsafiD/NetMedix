---
created_at: 2026-07-09
version_target: "2.0.0"
project: "NetMedix"
topic: "Desain Teknis Implementasi NetMedix v2.0.0"
tags: [expert-system, certainty-factor, netmedix, design, technical-spec]
related_files:
  - "[Perencanaan](./perencanaan-rombak-v2.0.0-NetMedix.md)"
  - "[TODO tasklist](./todo-rombak-v2.0.0-NetMedix.md)"
  - "[Discussion log](../../00_INBOX/2026-07-09_discussion-rombak-netmedix-pure-cf.md)"
status: "drafting"
ai_model: "Claude (glm-5)"
---

# Desain Teknis Implementasi NetMedix v2.0.0

> Dokumen ini menjawab **BAGAIMANA** implementasi v2.0.0. Untuk **APA/KENAPA** lihat `perencanaan-rombak-v2.0.0-NetMedix.md`.

---

## 1. Architecture Overview

### Before (v1.0.0)

```
data/*.json → KnowledgeBase → InferenceEngine (FC + CF) → top-3 results
                                   ↓
                        - calculate_cf_rule(MB, MD)
                        - AND-strict matching (issubset)
                        - combine sekuensial left-to-right
```

### After (v2.0.0)

```
data/*.json → KnowledgeBase → InferenceEngine (Pure CF) → all candidates (≥2 gejala)
                                   ↓
                        - cf_pakar dari riset multi-source langsung
                        - filter ≥ 2 gejala relevan dipilih user
                        - combine sekuensial left-to-right
                        - output mentah × 100, semua kandidat sort desc
```

**Komponen yang berubah:**
- `engine.py`: drop `calculate_cf_rule`, drop AND-strict, add filter ≥ 2 gejala, drop top-3
- `knowledge_base.py`: handle schema baru (cf_pakar, evidence, sources, tutorial)
- `app.py`: clamping [0.1, 1.0], route `/tutorial/<code>`
- `templates/symptoms.html`: tooltip + link tutorial
- `templates/diagnose.html`: radio 5 level
- `templates/result.html`: kesimpulan + semua kandidat
- `templates/tutorial.html`: BARU

---

## 2. Inference Engine Redesign

### A. Formula CF (Final — Locked)

**2 rumus saja** (drop `CF_rule = MB − MD`):

| # | Rumus | Lokasi kode |
|---|---|---|
| 1 | `CF_evidence = CF_user × CF_pakar` | `engine.py:calculate_cf_evidence` |
| 2 | `CF_combine = CF₁ + CF₂ × (1 − CF₁)` | `engine.py:combine_cf` |

**Asumsi yang valid:**
- CF_user selalu positif (range [0.1, 1.0])
- CF_pakar selalu positif (range [0.1, 1.0])
- Maka CF_evidence selalu positif
- Maka single-branch combine formula MYCIN tetap valid (tidak perlu 3 cabang)

### B. Pseudocode Algoritma `diagnose()`

```python
def diagnose(selected_symptoms: dict[str, float]) -> list[dict]:
    """
    Pure CF diagnosis dengan filter "≥ 2 gejala relevan".

    selected_symptoms: {"G01": 0.7, "G02": 1.0, ...}  # CF_user per gejala
    Returns: list of {
        problem_code, problem_name, rule_code,
        cf_final, percentage, label, matched_count,
        details: {evidence_steps, combine_steps}
    } sorted desc by cf_final. Empty if no problem passes filter.
    """
    results = []

    for rule in self.kb.rules:
        # Step 1: Identifikasi gejala relevan yang dipilih user
        rule_symptom_codes = {s["code"] for s in rule["symptoms"]}
        matched_codes = rule_symptom_codes & set(selected_symptoms.keys())

        # Step 2: FILTER — ≥ 2 gejala relevan dipilih
        if len(matched_codes) < 2:
            continue

        # Step 3: Hitung CF_evidence per matched gejala
        evidences = []
        for code in matched_codes:
            symptom_rule = next(s for s in rule["symptoms"] if s["code"] == code)
            cf_pakar = symptom_rule["cf_pakar"]
            cf_user = selected_symptoms[code]
            cf_ev = self.calculate_cf_evidence(cf_user, cf_pakar)
            evidences.append({
                "symptom_code": code,
                "cf_pakar": cf_pakar,
                "evidence_note": symptom_rule.get("evidence", ""),
                "cf_user": cf_user,
                "cf_evidence": cf_ev,
            })

        # Step 4: Combine sekuensial (fold left-to-right)
        cf_final, combine_steps = self._combine_cfs_with_trace(
            [e["cf_evidence"] for e in evidences]
        )

        # Step 5: Ambil problem info
        problem = self.kb.get_problem(rule["target_problem"])

        results.append({
            "problem_code": rule["target_problem"],
            "problem_name": problem["name"] if problem else "Unknown",
            "category": problem.get("category", ""),
            "rule_code": rule["code"],
            "rule_sources": rule.get("sources", []),
            "cf_final": cf_final,
            "percentage": round(cf_final * 100, 2),
            "label": self.interpret_cf(cf_final),
            "matched_count": len(matched_codes),
            "total_symptoms_in_rule": len(rule_symptom_codes),
            "details": {
                "evidence_steps": evidences,
                "combine_steps": combine_steps,
            },
        })

    # Sort desc, return ALL (no top-3 truncation)
    results.sort(key=lambda r: r["cf_final"], reverse=True)
    return results
```

### C. Helper: `_combine_cfs_with_trace`

```python
def _combine_cfs_with_trace(self, cf_list: list[float]) -> tuple[float, list[dict]]:
    """Combine list CF sekuensial, return (cf_final, trace_steps)."""
    if not cf_list:
        return 0.0, []

    combined = cf_list[0]
    steps = []
    for i, cf in enumerate(cf_list[1:], start=1):
        prev = combined
        combined = self.combine_cf(combined, cf)
        steps.append({
            "step": i,
            "cf_a": prev,
            "cf_b": cf,
            "result": combined,
        })
    return combined, steps
```

### D. Rename Function (Recommended)

- `forward_chaining()` → `diagnose()` — karena forward chaining tidak lagi relevan (tidak ada chaining antar rule, hanya per-symptom CF dalam satu rule).

### E. Drop yang Perlu Dihapus dari v1.0.0

| Lokasi v1.0.0 | Yang Dihapus |
|---|---|
| `engine.py:8-10` | `calculate_cf_rule(mb, md)` — fungsi & pemanggilan |
| `engine.py:36-37` | `if not rule_symptom_codes.issubset(...)` — AND-strict |
| `engine.py:42-54` | Block yang hitung `cf_rule = mb - md` |
| `engine.py:92` | `return results[:3]` — top-3 truncation |
| `engine.py:60-78` | Trace fields `mb`, `md`, `cf_rule` di evidence_steps |

---

## 3. Data Schema v2

### A. rules.json v2

```json
{
  "rules": [
    {
      "code": "R01",
      "name": "Aturan Tidak Ada Koneksi Jaringan",
      "target_problem": "P01",
      "sources": [
        "https://learn.microsoft.com/windows/client-management/...",
        "https://www.cisco.com/c/en/us/support/docs/...html",
        "https://support.apple.com/guide/mac-help/..."
      ],
      "symptoms": [
        {
          "code": "G01",
          "cf_pakar": 0.85,
          "evidence": "Primary indicator di MS Learn & Cisco docs"
        },
        {
          "code": "G20",
          "cf_pakar": 0.70,
          "evidence": "Common symptom di Cisco community forums"
        },
        {
          "code": "G26",
          "cf_pakar": 0.60,
          "evidence": "Differentiator isolated vs network-wide issue"
        }
      ]
    }
  ]
}
```

**Field baru:**
- Per rule: `sources` (array URL, **minimal 2 sumber independen**)
- Per gejala: `cf_pakar` (float 0.1-1.0), `evidence` (string justifikasi singkat)

**Field dihapus:** `mb`, `md` per gejala

**Validation rules:**
- Setiap rule wajib punya `code`, `name`, `target_problem`, `sources`, `symptoms`
- Setiap rule wajib punya minimal 2 symptoms (konsisten dengan filter "≥ 2 gejala")
- Setiap symptom wajib punya `code`, `cf_pakar` (0.1-1.0), `evidence`
- Setiap rule wajib punya ≥ 2 URL di `sources`

### B. symptoms.json v2

```json
{
  "symptoms": [
    {
      "code": "G14",
      "name": "Ping packet loss > 5%",
      "category": "Performa",
      "short_desc": "Saat ping ke server, lebih dari 5% paket gagal sampai",
      "how_to_check": "Buka CMD/Terminal → jalankan `ping 8.8.8.8 -n 20` → cek statistik packet loss di akhir",
      "tutorial": {
        "definition": "Packet loss adalah persentase paket data yang gagal mencapai tujuan. Threshold > 5% umum dianggap indikasi masalah jaringan (MS Learn, Cisco).",
        "verification_steps": [
          "Step 1: Buka CMD (Windows) atau Terminal (Linux/Mac)",
          "Step 2: Jalankan command `ping 8.8.8.8 -n 20` (atau `-c 20` di Linux/Mac)",
          "Step 3: Tunggu hingga selesai, lihat statistik akhir",
          "Step 4: Cek persentase pada baris 'Lost = X%'"
        ],
        "interpretation": "< 5% normal | 5-15% ada masalah | > 15% serius",
        "common_causes": [
          "Interferensi WiFi",
          "Kabel rusak/longgar",
          "Bandwidth saturation",
          "Hardware issue (NIC/switch)"
        ],
        "related_symptoms": ["G23", "G22"]
      }
    }
  ]
}
```

**Field baru per gejala:**
- `short_desc` (string, 1-2 kalimat)
- `how_to_check` (string, command/tool cepat)
- `tutorial` (object): `definition`, `verification_steps` (array), `interpretation`, `common_causes` (array), `related_symptoms` (array kode gejala)

### C. problems.json

Tidak berubah struktur signifikan. Mungkin update deskripsi jika perlu selama riset.

### D. Migration Plan

1. **Backup** data lama:
   - `data/rules.json` → `data/rules.v1.0.0.json.bak`
   - `data/symptoms.json` → `data/symptoms.v1.0.0.json.bak`
2. **Build ulang rules.json v2** berdasarkan tabel CF_pakar riset (`docs-NetMedix/tabel-cf-pakar-riset.md`)
3. **Expand symptoms.json v2** dengan konten tutorial hasil riset (bundling dengan Phase 1)
4. **Validate** JSON schema sebelum commit:
   - Pakai `jsonschema` validator atau script Python ad-hoc
   - Semua field required terisi
   - Range value valid

---

## 4. Backend Changes (app.py)

### A. Clamping CF_user

```python
# v1.0.0
cf_val = max(-1.0, min(1.0, cf_val))

# v2.0.0
cf_val = max(0.1, min(1.0, cf_val))
```

Lokasi: `app.py` sekitar line 180 (clamping di loop collect CF user).

### B. Route Baru: `/tutorial/<code>`

```python
@app.route("/tutorial/<code>")
def tutorial_page(code: str):
    """Halaman tutorial gejala per kode (G01-G40)."""
    code = code.upper()
    symptom = kb.get_symptom(code)  # NEW method di KnowledgeBase
    if not symptom:
        abort(404)

    # Resolve related_symptoms untuk link
    related = []
    for r_code in symptom.get("tutorial", {}).get("related_symptoms", []):
        r_symptom = kb.get_symptom(r_code)
        if r_symptom:
            related.append({"code": r_code, "name": r_symptom["name"]})

    return render_template(
        "tutorial.html",
        symptom=symptom,
        related=related,
    )
```

### C. Diagnosis Route Update

Adaptasi response engine baru di `/diagnose` route:

```python
results = engine.diagnose(selected_symptoms)  # ganti dari forward_chaining

# Build kesimpulan naratif
kesimpulan = build_kesimpulan(results)  # helper baru

return render_template(
    "result.html",
    results=results,           # ALL candidates (bukan top-3)
    kesimpulan=kesimpulan,     # narasi utama
    selected_symptoms=selected_symptoms,
    total_gejala_dipilih=len(selected_symptoms),
)
```

### D. Helper `build_kesimpulan`

```python
def build_kesimpulan(results: list[dict]) -> dict:
    """Build narasi kesimpulan untuk result.html."""
    if not results:
        return {
            "status": "empty",
            "message": "Tidak ada diagnosis yang memenuhi syarat (minimal 2 gejala relevan). "
                       "Coba pilih gejala tambahan yang lebih spesifik.",
        }

    top = results[0]
    others = results[1:4]  # tampilkan maks 3 alternatif di narasi

    return {
        "status": "found",
        "top_problem": top,
        "alternatives": others,
        "total_candidates": len(results),
    }
```

### E. Histori SQLite

Struktur tabel history tetap (id, timestamp, selected_symptoms_json, results_json). Karena results structure berubah, histori lama akan tetap render dengan caveat:

```python
# Saat render history
for item in history:
    try:
        results = json.loads(item["results_json"])
        # Cek apakah format v2 (ada 'percentage' field) atau v1 (ada 'cf_final' tanpa 'percentage')
        is_v2 = all("percentage" in r for r in results) if results else True
        item["is_v2"] = is_v2
    except Exception:
        item["is_v2"] = False
```

UI bisa flag "diagnosa v1" untuk histori lama.

---

## 5. Frontend Changes

### A. symptoms.html (Step 1 — Pilih Gejala)

**Komponen baru per item gejala:**

```html
<div class="symptom-item flex items-start gap-3">
  <input type="checkbox" name="symptoms" value="G14" id="sym_G14">
  <label for="sym_G14" class="flex-1">
    <span class="font-medium">Ping packet loss > 5%</span>
    <span class="text-gray-500 text-sm">(G14)</span>
  </label>

  <!-- Info button -->
  <button type="button"
          onclick="showSymptomInfo('G14')"
          class="info-btn"
          aria-label="Info gejala G14">
    ⓘ
  </button>
</div>
```

**Modal info (single modal, populated dynamically):**

```html
<div id="symptomModal" class="modal hidden">
  <div class="modal-content">
    <h3 id="modalTitle">G14 — Ping packet loss</h3>
    <p id="modalShortDesc" class="text-gray-700"></p>

    <div class="mt-4">
      <h4 class="font-medium">Cara cek:</h4>
      <p id="modalHowToCheck" class="text-sm font-mono bg-gray-100 p-2 rounded"></p>
    </div>

    <a id="modalTutorialLink" href="#" class="text-blue-600 underline mt-4 block">
      Pelajari lebih lanjut →
    </a>

    <button onclick="closeModal()" class="mt-4">Tutup</button>
  </div>
</div>
```

**JS:**
```javascript
const SYMPTOM_DATA = {{ symptoms_with_info | tojson }};

function showSymptomInfo(code) {
  const data = SYMPTOM_DATA[code];
  document.getElementById('modalTitle').textContent = `${code} — ${data.name}`;
  document.getElementById('modalShortDesc').textContent = data.short_desc;
  document.getElementById('modalHowToCheck').textContent = data.how_to_check;
  document.getElementById('modalTutorialLink').href = `/tutorial/${code}`;
  document.getElementById('symptomModal').classList.remove('hidden');
}
```

### B. diagnose.html (Step 2 — Pilih CF_user)

**Radio button 5 level per gejala yang sudah dipilih:**

```html
<fieldset class="cf-group" data-symptom="G14">
  <legend class="font-medium">G14 — Ping packet loss > 5%</legend>
  <p class="text-sm text-gray-600">Seberapa yakin Anda mengalami gejala ini?</p>

  <div class="radio-grid grid grid-cols-5 gap-2 mt-2">
    <label class="radio-card">
      <input type="radio" name="cf_G14" value="0.1">
      <span class="label-block">
        <span class="value">0.1</span>
        <span class="text">Hampir Tidak Yakin</span>
      </span>
    </label>
    <label class="radio-card">
      <input type="radio" name="cf_G14" value="0.3">
      <span class="label-block">
        <span class="value">0.3</span>
        <span class="text">Kurang Yakin</span>
      </span>
    </label>
    <label class="radio-card">
      <input type="radio" name="cf_G14" value="0.5" checked>
      <span class="label-block">
        <span class="value">0.5</span>
        <span class="text">Cukup Yakin</span>
      </span>
    </label>
    <label class="radio-card">
      <input type="radio" name="cf_G14" value="0.7">
      <span class="label-block">
        <span class="value">0.7</span>
        <span class="text">Yakin</span>
      </span>
    </label>
    <label class="radio-card">
      <input type="radio" name="cf_G14" value="1.0">
      <span class="label-block">
        <span class="value">1.0</span>
        <span class="text">Sangat Yakin</span>
      </span>
    </label>
  </div>
</fieldset>
```

**Default value:** `0.5` (Cukup Yakin) — pre-checked supaya user tidak lupa pilih.

### C. result.html (Hasil Diagnosis)

**Struktur baru:**

```html
<!-- 1. Section Kesimpulan (di atas) -->
<section class="kesimpulan bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
  {% if kesimpulan.status == "empty" %}
    <p>{{ kesimpulan.message }}</p>
  {% else %}
    <h2>Hasil Diagnosis</h2>
    <p class="text-lg">
      Berdasarkan gejala yang Anda pilih, sistem memperkirakan masalah utama:
      <strong>{{ kesimpulan.top_problem.problem_name }}</strong>
      dengan keyakinan
      <strong>{{ kesimpulan.top_problem.percentage }}%
             ({{ kesimpulan.top_problem.label }})</strong>.
    </p>
    {% if kesimpulan.alternatives %}
    <p class="text-sm text-gray-700 mt-2">
      Kandidat lain yang perlu dipertimbangkan:
      {% for alt in kesimpulan.alternatives %}
        {{ alt.problem_name }} ({{ alt.percentage }}%)
        {% if not loop.last %}, {% endif %}
      {% endfor %}
    </p>
    {% endif %}
    <p class="text-xs text-gray-500 mt-2">
      Total {{ kesimpulan.total_candidates }} kandidat teridentifikasi.
    </p>
  {% endif %}
</section>

<!-- 2. Section Detail Kandidat (semua, bukan top-3) -->
<section class="detail-kandidat">
  <h3>Detail Perhitungan per Kandidat</h3>
  {% for result in results %}
    <article class="kandidat-card mb-4 p-4 border rounded">
      <header class="flex justify-between">
        <h4>{{ result.problem_code }} — {{ result.problem_name }}</h4>
        <span class="badge">{{ result.percentage }}% · {{ result.label }}</span>
      </header>
      <p class="text-sm text-gray-600">
        Matched: {{ result.matched_count }}/{{ result.total_symptoms_in_rule }} gejala relevan
      </p>

      <!-- 3. Trace collapsible -->
      <details class="mt-2">
        <summary class="cursor-pointer text-blue-600">Lihat trace perhitungan</summary>
        <div class="trace-content mt-2 text-sm">
          <!-- evidence_steps table (adapted: no MB/MD, only cf_pakar) -->
          <!-- combine_steps table -->
        </div>
      </details>
    </article>
  {% endfor %}
</section>
```

### D. tutorial.html (BARU)

**Layout format mirip YAML frontmatter:**

```html
<article class="tutorial-page max-w-3xl mx-auto p-6">
  <!-- Back button -->
  <a href="/diagnose" class="text-blue-600 mb-4 inline-block">← Kembali ke form</a>

  <!-- YAML-like header -->
  <header class="yaml-header bg-gray-900 text-green-400 p-4 rounded font-mono text-sm">
    <div>code:           <span class="text-yellow-300">{{ symptom.code }}</span></div>
    <div>name:           <span class="text-yellow-300">{{ symptom.name }}</span></div>
    <div>category:       <span class="text-yellow-300">{{ symptom.category }}</span></div>
    <div>short_desc:     <span class="text-yellow-300">{{ symptom.short_desc }}</span></div>
  </header>

  <!-- Body content -->
  <div class="tutorial-body mt-6 space-y-6">
    <section>
      <h2 class="text-xl font-bold border-b pb-1">Definisi</h2>
      <p>{{ symptom.tutorial.definition }}</p>
    </section>

    <section>
      <h2 class="text-xl font-bold border-b pb-1">Cara Verifikasi</h2>
      <ol class="list-decimal list-inside space-y-1">
        {% for step in symptom.tutorial.verification_steps %}
          <li>{{ step }}</li>
        {% endfor %}
      </ol>
    </section>

    <section>
      <h2 class="text-xl font-bold border-b pb-1">Interpretasi Hasil</h2>
      <p>{{ symptom.tutorial.interpretation }}</p>
    </section>

    <section>
      <h2 class="text-xl font-bold border-b pb-1">Penyebab Umum</h2>
      <ul class="list-disc list-inside space-y-1">
        {% for cause in symptom.tutorial.common_causes %}
          <li>{{ cause }}</li>
        {% endfor %}
      </ul>
    </section>

    {% if related %}
    <section>
      <h2 class="text-xl font-bold border-b pb-1">Gejala Terkait</h2>
      <ul class="space-y-1">
        {% for rel in related %}
          <li>
            <a href="/tutorial/{{ rel.code }}" class="text-blue-600 underline">
              {{ rel.code }} — {{ rel.name }}
            </a>
          </li>
        {% endfor %}
      </ul>
    </section>
    {% endif %}
  </div>
</article>
```

**Styling:**
- Header YAML pakai dark background (gray-900) + monospace + syntax-highlighting warna
- Body section terpisah jelas dengan border-b
- Max-width constraint agar readable

---

## 6. Edge Cases Handling

| Skenario | Behavior v2.0.0 |
|---|---|
| User pilih 0 gejala | Form validation di Step 2: "Pilih minimal 1 gejala dulu" |
| User pilih hanya 1 gejala relevan ke problem X | Problem X **tidak muncul** di hasil (gagal filter ≥ 2). Tampil empty state. |
| User pilih gejala orphan (G31-G39 yang tidak masuk rule) | Gejala tsb tidak kontribusi ke problem manapun. Info di symptoms.html: "Gejala ini belum didukung sistem diagnosis" (opsional badge). |
| User input CF_user di luar [0.1, 1.0] | Clamp otomatis di backend (`max(0.1, min(1.0, cf_val))`) |
| User akses `/tutorial/G99` (kode tidak ada) | 404 Not Found page |
| User akses `/tutorial/g01` (lowercase) | Normalize `.upper()` → redirect ke `/tutorial/G01` |
| Cross-cutting gejala (G14, G23, G24) dipilih | Bisa trigger multiple problem, semua muncul di hasil sort desc |
| Histori diagnosis lama (v1 schema, ada field mb/md) | Lazy render di page histori, flag "diagnosa v1" (tanpa percentage field) |
| Rule dengan kurang dari 2 symptoms di KB | Tidak akan pernah fire (filter ≥ 2 tidak bisa terpenuhi). Validasi di Phase 2 harus pastikan semua rule punya ≥ 2 symptoms. |
| CF_combine overflow (> 1.0) | Tidak mungkin secara matematis: `CF₁ + CF₂(1 − CF₁)` dengan CF₁,CF₂ ∈ [0,1] selalu ≤ 1 |

---

## 7. Testing Strategy

### A. Unit Test Engine (6 skenario)

| Test | Input | Expected Output |
|---|---|---|
| **T1 — Single symptom P12** | `{G15: 0.7}` | P12 muncul? **TIDAK** (gagal filter ≥ 2). Empty result. |
| **T2 — Multi-symptom P15** | `{G19: 1.0, G27: 0.8, G34: 1.0}` | P15 CF sesuai manual calc |
| **T3 — 1 gejala relevan** | `{G02: 0.7}` saja | Empty (P02 butuh ≥ 2) |
| **T4 — 0 gejala** | `{}` | Empty result |
| **T5 — Orphan gejala saja** | `{G31: 0.7}` | Empty (G31 tidak di rule manapun) |
| **T6 — Cross-cutting** | `{G14: 0.9, G23: 0.7, G18: 0.8, G29: 0.9}` | P11 (G14+G23) DAN P14 (G18+G29+G14) muncul, sort desc |

Manual calc reference untuk T2 (P15) akan diambil dari tabel CF_pakar hasil riset.

### B. Integration Test via Chrome Devtools MCP (8 skenario)

| E2E | Skenario | Verifikasi |
|---|---|---|
| **E2E-1** | User flow lengkap: home → symptoms → diagnose → result | Semua halaman render tanpa error, URL flow benar |
| **E2E-2** | Klik ⓘ info icon di gejala | Modal tampil dengan short_desc + how_to_check + link tutorial |
| **E2E-3** | Klik link "Pelajari lebih lanjut" | Halaman `/tutorial/<code>` tampil dengan layout YAML-like |
| **E2E-4** | Skenario P02 (Internet putus): centang G02, G03, G28 → CF 1.0/1.0/0.8 → submit | Diagnosis P02 muncul di top, percentage mendekati manual calc |
| **E2E-5** | Skenario P05 (DHCP failure): centang G05, G30, G40 → CF tinggi → submit | Diagnosis P05 muncul di top |
| **E2E-6** | Skenario < 2 gejala relevan: centang hanya G02 → submit | Halaman result tampilkan empty state, bukan error |
| **E2E-7** | Akses halaman histori diagnosis | Histori tampil, baik entry v1 (lama) maupun v2 (baru) |
| **E2E-8** | Resize viewport ke mobile (375px) | Semua halaman tetap readable, tidak overflow horizontal |

**Untuk setiap E2E:**
- Screenshot di-capture
- Console messages di-cek (tidak boleh ada error)
- Network requests di-cek (status 200 untuk assets)

**Lighthouse audit:**
- Accessibility ≥ 90
- Best Practices ≥ 90
- (Performance tidak jadi blocker untuk tugas kuliah)

### C. Validation Rules (JSON Schema)

Pakai validator `jsonschema` Python:

```python
RULES_SCHEMA_V2 = {
    "type": "object",
    "required": ["rules"],
    "properties": {
        "rules": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["code", "name", "target_problem", "sources", "symptoms"],
                "properties": {
                    "code": {"type": "string", "pattern": "^R\\d{2}$"},
                    "name": {"type": "string"},
                    "target_problem": {"type": "string", "pattern": "^P\\d{2}$"},
                    "sources": {
                        "type": "array",
                        "minItems": 2,
                        "items": {"type": "string", "format": "uri"}
                    },
                    "symptoms": {
                        "type": "array",
                        "minItems": 2,
                        "items": {
                            "type": "object",
                            "required": ["code", "cf_pakar", "evidence"],
                            "properties": {
                                "code": {"type": "string", "pattern": "^G\\d{2}$"},
                                "cf_pakar": {"type": "number", "minimum": 0.1, "maximum": 1.0},
                                "evidence": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

*Status: drafting | Implementasi setelah Fase 1 (riset) selesai dan tabel CF_pakar final*
