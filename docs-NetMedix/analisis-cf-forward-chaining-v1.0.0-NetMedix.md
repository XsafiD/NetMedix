---
created_at: 2026-07-06
topic: "Analisis Implementasi Certainty Factor & Forward Chaining pada NetMedix v1.0.0"
tags: [expert-system, certainty-factor, forward-chaining, inference-engine, sistem-cerdas, netmedix, mycin]
source_urls:
  - "file://04_TUGAS/NetMedix/inference/engine.py"
  - "file://04_TUGAS/NetMedix/inference/knowledge_base.py"
  - "file://04_TUGAS/NetMedix/data/rules.json"
  - "file://04_TUGAS/NetMedix/app.py"
  - "file://04_TUGAS/NetMedix/docs/VERSION-CONTROL.md"
suggested_location: "03_RISET"
status: inbox
ai_model: "Claude (glm-5)"
related_project: "04_TUGAS/NetMedix @ v1.0.0"
---

# Analisis Implementasi Certainty Factor & Forward Chaining — NetMedix v1.0.0

> Sistem pakar diagnosis masalah jaringan komputer berbasis web (Flask) yang menggabungkan **Forward Chaining** sebagai controller inferensi dan **Certainty Factor** sebagai kalkulator kepercayaan.

---

## Executive Summary

NetMedix v1.0.0 adalah aplikasi web hasil UAS mata kuliah Sistem Cerdas yang mengimplementasikan sistem pakar diagnosis masalah jaringan komputer. Sistem menggunakan kombinasi dua metode klasik AI:

1. **Forward Chaining (data-driven reasoning)** — memutuskan rule mana yang "fire" berdasarkan kelengkapan gejala input dari user.
2. **Certainty Factor (CF)** — varian sederhana dari CF MYCIN (Shortliffe & Buchanan) untuk mengakumulasi keyakinan user × ahli menjadi skor akhir 0–100%.

Knowledge base terdiri dari **15 problem**, **40 gejala**, dan **15 aturan IF-THEN** dengan bobot MB/MD per gejala. Implementasi inti berada di `inference/engine.py` (115 baris) yang clean, modular, dan mengembalikan trace perhitungan step-by-step untuk explainability.

---

## 1. Arsitektur Singkat

```
data/*.json  →  KnowledgeBase  →  InferenceEngine  →  Hasil Diagnosis
(aturan)        (loader)            (CF + FC)           (top 3)
```

Knowledge base dipisah dari inference engine — pola **separation of concerns** yang bersih. Data aturan disimpan dalam JSON, bukan di-hardcode di Python. Hal ini membuat aturan dapat di-edit lewat admin panel tanpa menyentuh kode.

### File Inti

| File | Lokasi | Baris | Fungsi |
|------|--------|-------|--------|
| `inference/engine.py` | 04_TUGAS/NetMedix/ | 115 | Implementasi Forward Chaining + CF |
| `inference/knowledge_base.py` | 04_TUGAS/NetMedix/ | 65 | Loader & query untuk JSON KB |
| `data/problems.json` | 04_TUGAS/NetMedix/ | — | 15 masalah jaringan (P01–P15) |
| `data/symptoms.json` | 04_TUGAS/NetMedix/ | — | 40 gejala (G01–G40) |
| `data/rules.json` | 04_TUGAS/NetMedix/ | — | 15 aturan IF-THEN + MB/MD (R01–R15) |
| `app.py` | 04_TUGAS/NetMedix/ | 637 | Flask routes, DB, CRUD, diagnosis flow |

---

## 2. Struktur Knowledge Base

Tiap rule di `data/rules.json` memetakan **satu problem** dengan **multiple symptoms**, masing-masing punya bobot MB/MD:

```json
{
  "code": "R01",
  "name": "Aturan Tidak Ada Koneksi Jaringan",
  "target_problem": "P01",
  "symptoms": [
    { "code": "G01", "mb": 0.9, "md": 0.1 },
    { "code": "G20", "mb": 0.8, "md": 0.1 },
    { "code": "G26", "mb": 0.7, "md": 0.1 }
  ]
}
```

### Definisi Bobot

| Simbol | Nama | Range | Makna |
|--------|------|-------|-------|
| **MB** | Measure of Belief | [0, 1] | Keyakinan ahli bahwa gejala menopong hipotesis |
| **MD** | Measure of Disbelief | [0, 1] | Ketidakpercayaan ahli terhadap hipotesis |
| **CF_user** | User Certainty | [-1, 1] | Tingkat keyakinan user (dari radio button Step 2) |

### Statistik KB

| Entitas | Jumlah | Status |
|---------|--------|--------|
| Masalah Jaringan | 15 | P01–P15, 7 kategori |
| Gejala | 40 | G01–G40, 7 kategori |
| Aturan IF-THEN | 15 | R01–R15, 1 rule per problem |
| Nilai MB/MD | 48 pasang | Difinalisasi dari riset |

---

## 3. Rumus Certainty Factor yang Dipakai

NetMedix mengimplementasikan **3 rumus inti CF** (varian klasik Shortliffe & Buchanan untuk MYCIN):

### a) CF Rule — keyakinan ahli per gejala

**Lokasi:** `inference/engine.py:7-10`

$$CF_{rule}(H,E) = MB - MD$$

```python
@staticmethod
def calculate_cf_rule(mb, md):
    """Hitung CF rule: CF(H,E) = MB - MD."""
    return mb - md
```

**Contoh** untuk R01/G01: `0.9 − 0.1 = 0.8`

---

### b) CF Evidence — gabungan keyakinan ahli × user

**Lokasi:** `inference/engine.py:12-15`

$$CF_{evidence} = CF_{user} \times CF_{rule}(H,E)$$

```python
@staticmethod
def calculate_cf_evidence(cf_user, cf_rule):
    """Hitung CF evidence: CF_evidence = CF_user x CF(H,E)."""
    return cf_user * cf_rule
```

`CF_user` adalah nilai 0–1 yang dipilih user di Step 2 (Sangat Yakin=1.0, Yakin=0.8, Cukup=0.6, dll). Filter clamp dilakukan di `app.py:180`:

```python
cf_val = max(-1.0, min(1.0, cf_val))
```

---

### c) CF Combine — kombinasi beberapa evidence

**Lokasi:** `inference/engine.py:17-20`

$$CF_{combine}(CF_1, CF_2) = CF_1 + CF_2 \times (1 - CF_1)$$

```python
@staticmethod
def combine_cf(cf1, cf2):
    """Kombinasi dua nilai CF: CF_combine = CF1 + CF2 x (1 - CF1)."""
    return cf1 + cf2 * (1 - cf1)
```

Kombinasi dilakukan **bertahap (reduce left-to-right)** di `inference/engine.py:94-101`: ambil evidence pertama sebagai accumulator, lalu fold dengan evidence berikutnya.

```python
def _combine_cfs(self, cf_list):
    """Kombinasikan list CF menggunakan rumus bertahap."""
    if not cf_list:
        return 0.0
    combined = cf_list[0]
    for cf in cf_list[1:]:
        combined = self.combine_cf(combined, cf)
    return combined
```

> **Catatan teoretis:** Rumus resmi MYCIN membagi 2 cabang berdasarkan tanda CF (sama positif / sama negatif / berlawanan tanda). NetMedix memakai **versi yang disederhanakan** — cukup satu rumus untuk semua kasus. Pendekatan ini aman karena di KB nilai MD kecil (≤ 0.3) sehingga `CF_evidence` hampir selalu positif. Pola ini umum di buku ajar Sistem Cerdas lokal (Kusumadewi 2003, Bab 5).

---

## 4. Forward Chaining — Algoritma

**Lokasi:** `inference/engine.py:22-92`. Forward chaining di sini berjenis **data-driven** (faktanya nyaris mirip rule matching, karena tiap rule langsung ke problem unik).

### Alur Langkah-demi-Langkah

| Langkah | Lokasi | Deskripsi |
|---|---|---|
| 1. Iterasi semua rule | `engine.py:32` | `for rule in self.kb.rules` |
| 2. Cek precondition | `engine.py:33-37` | Rule "fire" **hanya jika semua gejala rule ⊆ input user** (pakai `issubset`) |
| 3. Hitung CF per gejala | `engine.py:42-54` | `cf_rule = MB − MD`, lalu `cf_evidence = cf_user × cf_rule` |
| 4. Kombinasi bertahap | `engine.py:57` → `_combine_cfs` | Fold semua `cf_evidence` dengan `combine_cf` |
| 5. Simpan detail trace | `engine.py:60-78` | `evidence_steps` & `combine_steps` untuk transparansi |
| 6. Sort & ambil top 3 | `engine.py:91-92` | `results.sort(reverse=True)[:3]` |

### Logika Keputusan "Rule Fire" (Precondition)

```python
rule_symptom_codes = {s["code"] for s in rule["symptoms"]}
if not rule_symptom_codes.issubset(set(selected_symptoms.keys())):
    continue   # lewati rule jika ada satu gejala pun belum dipilih user
```

Ini berarti strategi matching-nya **AND ketat (conjunctive)** — bukan partial match. Konsekuensinya: jika user melewatkan 1 gejala dari rule, diagnosis itu tidak muncul sama sekali. Strategi cocok untuk domain troubleshooting jaringan di mana rangkaian gejala harus lengkap untuk konfirmasi masalah.

### Signature Fungsi

```python
def forward_chaining(self, selected_symptoms):
    """
    Run forward chaining on selected symptoms.

    selected_symptoms: dict { "G01": cf_user_value, "G02": cf_user_value, ... }
    Returns: list of {"problem_code": str, "cf_final": float, "details": dict}
             sorted by CF descending, top 3.
    """
```

---

## 5. Trace Output per Diagnosis (Explainability)

Engine mengembalikan struktur detail yang **replay-able**, dipakai template `result.html` untuk menampilkan langkah hitung. Ini membuat sistem transparan — user bisa mengaudit angka final, bukan menerima black-box.

```python
{
  "problem_code": "P02",
  "rule_code": "R02",
  "rule_name": "Aturan Koneksi Internet Terputus",
  "cf_final": 0.9542,
  "details": {
    "evidence_steps": [
      {
        "symptom_code": "G02",
        "mb": 0.8, "md": 0.1,
        "cf_rule": 0.7,
        "cf_user": 0.8,
        "cf_evidence": 0.56
      },
      ...
    ],
    "combine_steps": [
      { "step": 1, "cf_a": 0.560, "cf_b": 0.800, "result": 0.9120 },
      { "step": 2, "cf_a": 0.912, "cf_b": 0.480, "result": 0.9542 }
    ]
  }
}
```

---

## 6. Interpretasi CF → Label Linguistik

**Lokasi:** `inference/engine.py:103-115`. CF diskala ke kategori linguistik untuk konsumsi user.

| CF Final | Label | Keterangan |
|---|---|---|
| ≥ 0.80 | **Sangat Yakin** | Diagnosis sangat mungkin |
| ≥ 0.60 | **Cukup Yakin** | Diagnosis kemungkinan besar |
| ≥ 0.40 | **Kemungkinan** | Cukup indikasi, perlu cek |
| ≥ 0.20 | **Kurang Yakin** | Indikasi lemah |
| < 0.20 | **Tidak Yakin** | Tidak ada indikasi kuat |

Threshold ini dipakai juga di `app.py:202` (saat proses diagnosis) dan `app.py:277` (untuk histori).

---

## 7. Contoh Perhitungan Nyata (R02 → P02)

**Skenario:** User pilih G02=0.8, G03=1.0, G28=0.6 (sesuai test case v0.4.0-dev).

### Step 1 — CF Rule per Gejala

```
G02: CF_rule = 0.8 − 0.1 = 0.70  →  CF_evidence = 0.70 × 0.8 = 0.560
G03: CF_rule = 0.9 − 0.1 = 0.80  →  CF_evidence = 0.80 × 1.0 = 0.800
G28: CF_rule = 0.9 − 0.1 = 0.80  →  CF_evidence = 0.80 × 0.6 = 0.480
```

### Step 2 — Combine Bertahap

```
combine(0.560, 0.800) = 0.560 + 0.800 × (1 − 0.560) = 0.9120
combine(0.912, 0.480) = 0.912 + 0.480 × (1 − 0.912) = 0.9542
```

### Step 3 — Hasil Akhir

```
CF_final = 0.9542 → 95.42% → Label: "Sangat Yakin"
Problem: P02 — Koneksi Internet Terputus
```

### Skenario Test Lainnya (v1.0.0 Phase 13)

| Skenario | Input | Output | Status |
|---|---|---|---|
| S1: DNS down | G04=1.0, G21=1.0, G24=1.0 | P03 CF=99.8% | PASS |
| S2: WiFi lemah | G11=0.6, G12=0.4 | P09 CF=63.2% | PASS |
| S3: Router mati | G19=1.0, G27=0.8, G34=1.0 | P15 CF=99.56% | PASS |
| S4: IP conflict | G06=1.0, G23=0.6 | P06 CF=100.0% | PASS |
| S5: DHCP failure | G05=1.0, G30=1.0, G40=0.6 | P05 CF=98.6% | PASS |
| S6: Single symptom | G23=0.8 (alone) | No rule triggered | PASS |

---

## 8. Pengamatan Teknis & Catatan Kritis

Beberapa observasi penting dari analisis kode:

1. **CF simplifikasi** — Tidak ada penanganan kasus CF berlawanan tanda (CF positif + CF negatif). Aman selama bobot KB seperti sekarang (MD ≤ 0.3), tapi bisa memberi hasil non-intuitif kalau MD diperbesar di atas MB.

2. **Forward chaining AND-strict** — `issubset` di `engine.py:36` membuat coverage diagnosa sangat bergantung pada kelengkapan input. Alternatif umum: partial match dengan threshold, tapi tidak dipakai di sini. Ini trade-off precision vs recall yang disengaja.

3. **Top-3 truncation** — `results[:3]` mengembalikan maksimal 3 kemungkinan. Ini desain UX, bukan batasan teoretis.

4. **Knowledge base reload setiap request** — `KnowledgeBase()` di-instantiate ulang tiap request (`app.py:190`, `app.py:232`, dll). Fine untuk tugas kuliah, tidak ideal untuk traffic tinggi (perlu caching).

5. **Tidak ada konflik resolusi** — Karena tiap rule men-target unik problem (1:1), tidak ada dua rule kompetisi untuk hipotesis yang sama. Sehingga rumus combine hanya dipakai **intra-rule** (antar gejala di rule yang sama), bukan **inter-rule** untuk problem yang sama. Ini simplifikasi yang valid untuk struktur KB NetMedix.

6. **Clamping input** — `app.py:180` melakukan `max(-1.0, min(1.0, cf_val))` untuk menjaga CF_user dalam range teoretis [-1, 1]. Defensive coding yang baik.

---

## 9. Teknologi & Stack

| Layer | Teknologi | Keterangan |
|-------|-----------|------------|
| Backend | Python 3.10+ / Flask 3.1.3 | Inference engine pure Python |
| Frontend CSS | Tailwind CSS 3.x | CDN, zero build step |
| Frontend JS | Vanilla JS | Tab switching, checkbox sync |
| Font | Inter (Google Fonts) | Open-source mendekati Circular |
| Icons | Lucide Icons | CDN |
| Template | Jinja2 | Bundled with Flask |
| Knowledge Base | JSON files | Manual edit via admin panel |
| History DB | SQLite 3 | Python stdlib |
| Deployment | Flask dev server | `python app.py` → localhost:5000 |

---

## 10. Referensi & Konteks Teoretis

### Buku Ajar Terkait (yang ada di 03_RISET)

| Konsep | Referensi Utama | Lokasi |
|-------|-----------------|--------|
| Forward Chaining | AIMA (Russell & Norvig, Bab 7-10) | `03_RISET/2026-03-13_artificial-intelligence-modern-approach.md` |
| Certainty Factor | Kusumadewi 2003 (Bab 5) | `03_RISET/2026-03-13_artificial-intelligence-kusumadewi-2003.md` |
| Expert Systems | Negnevitsky (Bab 2-5) | `03_RISET/2026-03-13_artificial-intelligence-negnevitsky.md` |
| Hybrid CF + Forward Chaining | Vinod Chandra (PHI) | `03_RISET/2026-03-13_artificial-intelligence-vinod-chandra-phi-2020.md` |

### Asal Rumus CF

Varian CF yang dipakai NetMedix merujuk pada **MYCIN** (Shortliffe & Buchanan, 1975) yang disederhanakan. Rumus kombinasi yang dipakai:

$$CF_{combine} = CF_1 + CF_2 \times (1 - CF_1)$$

adalah kasus khusus untuk dua CF dengan tanda sama (keduanya positif). MYCIN asli memiliki 3 cabang:

| Kasus | Rumus MYCIN Asli |
|-------|------------------|
| CF₁ > 0, CF₂ > 0 | `CF₁ + CF₂(1 − CF₁)` ← dipakai NetMedix |
| CF₁ < 0, CF₂ < 0 | `CF₁ + CF₂(1 + CF₁)` |
| Tanda berbeda | `CF₁ + CF₂ / min(1, 1 − |CF₁||CF₂|)` |

NetMedix cukup memakai cabang pertama karena nilai MD di KB kecil.

---

## 11. Ringkasan

NetMedix v1.0.0 menggabungkan **forward chaining sebagai controller** (memutuskan rule mana yang fire berdasar kelengkapan gejala) dan **certainty factor sebagai kalkulator kepercayaan** (mengakumulasi keyakinan user × ahli menjadi skor akhir).

**Tiga rumus inti:**

```
CF_rule      = MB − MD                          (keyakinan ahli per gejala)
CF_evidence  = CF_user × CF_rule                (gabungan user × ahli)
CF_combine   = CF₁ + CF₂ × (1 − CF₁)            (akumulasi multi-evidence)
```

Implementasi clean, modular, dan explainable — trace perhitungan disimpan untuk audit. Cocok sebagai referensi pembelajaran sistem pakar dengan CF untuk mahasiswa Sistem Cerdas.

---

*Dibuat: 2026-07-06 | Project: NetMedix v1.0.0 | Lokasi saran: 03_RISET*
