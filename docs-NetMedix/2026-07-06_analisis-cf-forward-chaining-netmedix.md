---
created_at: 2026-07-06
topic: "Analisis Tabel Penyakit, Gejala & Aturan Forward Chaining NetMedix"
tags: [certainty-factor, forward-chaining, expert-system, netmedix, sistem-cerdas, mycin, knowledge-base]
source_urls:
  - "file://04_TUGAS/NetMedix/data/problems.json"
  - "file://04_TUGAS/NetMedix/data/symptoms.json"
  - "file://04_TUGAS/NetMedix/data/rules.json"
  - "file://04_TUGAS/NetMedix/inference/engine.py"
related_files:
  - "Analisis implementasi sebelumnya: [analisis-cf-forward-chaining-v1.0.0-NetMedix.md](../04_TUGAS/NetMedix/analisis-cf-forward-chaining-v1.0.0-NetMedix.md)"
  - "Riset teori CF: [2026-04-23_certainty-factor.md](../03_RISET/2026-04-23_certainty-factor.md)"
  - "Riset sistem pakar: [2026-04-09_sistem-pakar-expert-system.md](../03_RISET/2026-04-09_sistem-pakar-expert-system.md)"
suggested_location: "03_RISET"
status: inbox
ai_model: "Claude (glm-5)"
related_project: "04_TUGAS/NetMedix @ v1.0.0"
---

# Analisis Tabel Penyakit, Gejala & Aturan Forward Chaining NetMedix

> Dokumen ini berisi analisis komprehensif knowledge base NetMedix v1.0.0 dengan fokus pada **tabel Certainty Factor (MB/MD/CF Rule)** per gejala dan struktur **aturan Forward Chaining** (IF-THEN). Dokumen pelengkap dari [analisis implementasi sebelumnya](analisis-cf-forward-chaining-v1.0.0-NetMedix.md).

---

## Executive Summary

Analisis ini memetakan secara tabular seluruh komponen knowledge base NetMedix:

- **15 Penyakit** jaringan (P01–P15) terbagi dalam 7 kategori.
- **40 Gejala** (G01–G40), namun hanya **33 yang terpakai** di rule (7 orphan).
- **15 Aturan IF-THEN** (R01–R15) dengan logika **AND-strict**.
- **36 pasangan gejala–penyakit** dengan bobot MB/MD.
- **CF Rule tertinggi = 1.0** (G06 pada R06), **terendah = 0.2** (G23 pada R11, G14 pada R14).
- **3 gejala cross-cutting** (G14, G23, G24) yang muncul di lebih dari satu rule.
- **7 gejala orphan** (G31, G32, G33, G36, G37, G38, G39) tidak masuk rule manapun.

Implementasi CF mengikuti formula MYCIN (Shortliffe & Buchanan) yang disederhanakan: single-branch combine formula. Karena seluruh MD ≤ 0.3, simplifikasi ini aman.

---

## 1. Ringkasan Statistik

| Komponen | Jumlah | File Sumber |
|---|---|---|
| Penyakit / Problem (P) | 15 | `data/problems.json` |
| Gejala (G) | 40 | `data/symptoms.json` |
| Aturan Forward Chaining (R) | 15 | `data/rules.json` |
| Rule–Symptom pair total | 36 | — |
| Gejala terpakai | 33 dari 40 | — |
| Gejala **tidak terpakai** (orphan) | 7 | lihat §8 |

---

## 2. Tabel Penyakit (P01–P15)

| Kode | Nama Penyakit | Kategori |
|---|---|---|
| P01 | Tidak Ada Koneksi Jaringan | Konektivitas Dasar |
| P02 | Koneksi Internet Terputus | Konektivitas Dasar |
| P03 | DNS Resolution Failure | DNS |
| P04 | DNS Cache Poisoning / Hijacking | DNS |
| P05 | DHCP Failure | DHCP & IP Config |
| P06 | IP Address Conflict | DHCP & IP Config |
| P07 | Subnet Mask / Default Gateway Salah | DHCP & IP Config |
| P08 | Tidak Bisa Connect ke WiFi | WiFi |
| P09 | WiFi Signal Lemah / Interferensi | WiFi |
| P10 | Jaringan Lambat / Bandwidth Saturation | Performa |
| P11 | Packet Loss Tinggi | Performa |
| P12 | Latensi Tinggi / Jitter | Performa |
| P13 | Firewall Memblokir Koneksi | Keamanan |
| P14 | Kerusakan Kabel / Konektor Jaringan | Hardware |
| P15 | Kerusakan / Misconfiguration Router-Switch | Hardware |

**Distribusi kategori:** Konektivitas (2), DNS (2), DHCP/IP (3), WiFi (2), Performa (3), Keamanan (1), Hardware (2).

---

## 3. Tabel Gejala (G01–G40)

| Kode | Nama Gejala | Kategori |
|---|---|---|
| G01 | Tidak ada koneksi sama sekali | Konektivitas |
| G02 | Tidak bisa akses internet | Konektivitas |
| G03 | Bisa ping gateway, tidak bisa ping internet | Konektivitas |
| G04 | Bisa ping IP publik, tidak bisa akses domain | DNS |
| G05 | IP address 169.254.x.x (APIPA) | DHCP & IP Config |
| G06 | Pesan IP address conflict | DHCP & IP Config |
| G07 | Subnet mask berbeda dari device lain | DHCP & IP Config |
| G08 | Tidak ada default gateway | DHCP & IP Config |
| G09 | Tidak bisa connect ke WiFi | WiFi |
| G10 | SSID WiFi tidak muncul | WiFi |
| G11 | WiFi signal bar 1–2 | WiFi |
| G12 | WiFi sering disconnect | WiFi |
| G13 | Kecepatan internet sangat lambat | Performa |
| G14 | Ping packet loss > 5% | Performa |
| G15 | Ping time > 100ms lokal | Performa |
| G16 | Aplikasi tertentu tidak bisa connect | Keamanan |
| G17 | Website redirect ke halaman aneh | DNS |
| G18 | Link lamp NIC/switch mati/berkedip | Hardware |
| G19 | Semua client di jaringan terdampak | Hardware |
| G20 | Status NIC "Media Disconnected" | Konektivitas |
| G21 | DNS server tidak respond saat nslookup | DNS |
| G22 | Speed test hasil sangat rendah | Performa |
| G23 | Koneksi putus-nyala (intermittent) | Performa |
| G24 | Hanya bisa akses via IP, bukan domain | DNS |
| G25 | Firewall memblokir aplikasi | Keamanan |
| G26 | Device lain di jaringan normal | Konektivitas |
| G27 | Koneksi normal setelah restart router | Hardware |
| G28 | Lampu WAN router merah | Konektivitas |
| G29 | Kabel terlihat rusak / longgar | Hardware |
| G30 | Device tidak mendapat IP DHCP | DHCP & IP Config |
| G31 | VPN tidak bisa connect | Keamanan |
| G32 | VPN connect, resource internal tidak bisa diakses | Keamanan |
| G33 | Lampu LAN di router mati | Hardware |
| G34 | Router tidak respond saat diakses | Hardware |
| G35 | Error "Destination Host Unreachable" | Konektivitas |
| G36 | Network adapter disabled | Konektivitas |
| G37 | Driver network adapter bermasalah | Konektivitas |
| G38 | Hanya satu perangkat yang bermasalah | Konektivitas |
| G39 | Proxy setting aktif tanpa sepengetahuan | Konektivitas |
| G40 | Error "Limited Connectivity" | DHCP & IP Config |

---

## 4. Tabel Aturan Forward Chaining (R01–R15)

Format logis: **IF** (gejala-1 ∧ gejala-2 ∧ ...) **THEN** Penyakit.

| Rule | Target | Antecedent (IF — semua gejala harus dipenuhi) | THEN |
|---|---|---|---|
| R01 | P01 | G01 ∧ G20 ∧ G26 | Tidak Ada Koneksi Jaringan |
| R02 | P02 | G02 ∧ G03 ∧ G28 | Koneksi Internet Terputus |
| R03 | P03 | G04 ∧ G21 ∧ G24 | DNS Resolution Failure |
| R04 | P04 | G17 ∧ G24 | DNS Cache Poisoning / Hijacking |
| R05 | P05 | G05 ∧ G30 ∧ G40 | DHCP Failure |
| R06 | P06 | G06 ∧ G23 | IP Address Conflict |
| R07 | P07 | G07 ∧ G08 ∧ G35 | Subnet Mask / Gateway Salah |
| R08 | P08 | G09 ∧ G10 | Tidak Bisa Connect WiFi |
| R09 | P09 | G11 ∧ G12 | WiFi Signal Lemah |
| R10 | P10 | G13 ∧ G22 | Jaringan Lambat |
| R11 | P11 | G14 ∧ G23 | Packet Loss Tinggi |
| R12 | P12 | G15 (single symptom) | Latensi Tinggi / Jitter |
| R13 | P13 | G16 ∧ G25 | Firewall Memblokir |
| R14 | P14 | G18 ∧ G29 ∧ G14 | Kerusakan Kabel / Konektor |
| R15 | P15 | G19 ∧ G27 ∧ G34 | Kerusakan / Misconfig Router-Switch |

**Sifat logic:** AND-strict — implementasi di `inference/engine.py:36` menggunakan `rule_symptom_codes.issubset(selected_symptoms)`. Rule hanya "fire" bila **semua** gejala pada antecedent dipilih user.

---

## 5. Tabel Certainty Factor (MB / MD / CF Rule) — Detail per Gejala

Rumus: `CF_rule(H,E) = MB − MD` (Shortliffe & Buchanan, MYCIN), diimplementasikan di `inference/engine.py:10`.

### R01 → P01 (Tidak Ada Koneksi Jaringan)

| Symptom | MB | MD | CF Rule | Interpretasi Keyakinan Pakar |
|---|---|---|---|---|
| G01 (tidak ada koneksi) | 0.9 | 0.1 | **0.8** | Sangat yakin |
| G20 (Media Disconnected) | 0.8 | 0.1 | **0.7** | Yakin |
| G26 (device lain normal) | 0.7 | 0.1 | **0.6** | Cukup yakin |

### R02 → P02 (Koneksi Internet Terputus)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G02 (tidak bisa akses internet) | 0.8 | 0.1 | **0.7** |
| G03 (ping gateway ok, internet gagal) | 0.9 | 0.1 | **0.8** |
| G28 (lampu WAN merah) | 0.9 | 0.1 | **0.8** |

### R03 → P03 (DNS Resolution Failure)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G04 (ping IP ok, domain gagal) | 0.9 | 0.0 | **0.9** |
| G21 (DNS tidak respond nslookup) | 0.9 | 0.1 | **0.8** |
| G24 (akses via IP saja) | 0.9 | 0.0 | **0.9** |

### R04 → P04 (DNS Cache Poisoning)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G17 (redirect halaman aneh) | 0.8 | 0.3 | **0.5** |
| G24 (akses via IP saja) | 0.6 | 0.1 | **0.5** |

### R05 → P05 (DHCP Failure)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G05 (IP 169.254.x.x) | 0.9 | 0.0 | **0.9** |
| G30 (tidak dapat DHCP) | 0.9 | 0.1 | **0.8** |
| G40 (Limited Connectivity) | 0.7 | 0.2 | **0.5** |

### R06 → P06 (IP Address Conflict)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G06 (pesan IP conflict) | 1.0 | 0.0 | **1.0** ⭐ tertinggi |
| G23 (intermittent) | 0.6 | 0.3 | **0.3** |

### R07 → P07 (Subnet/Gateway Salah)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G07 (subnet mask beda) | 0.9 | 0.0 | **0.9** |
| G08 (tidak ada gateway) | 0.8 | 0.1 | **0.7** |
| G35 (Destination Host Unreachable) | 0.6 | 0.3 | **0.3** |

### R08 → P08 (Tidak Bisa Connect WiFi)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G09 (tidak bisa connect WiFi) | 0.8 | 0.1 | **0.7** |
| G10 (SSID tidak muncul) | 0.7 | 0.2 | **0.5** |

### R09 → P09 (WiFi Signal Lemah)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G11 (signal 1–2 bar) | 0.9 | 0.0 | **0.9** |
| G12 (sering disconnect) | 0.7 | 0.2 | **0.5** |

### R10 → P10 (Jaringan Lambat)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G13 (sangat lambat) | 0.8 | 0.1 | **0.7** |
| G22 (speed test rendah) | 0.9 | 0.0 | **0.9** |

### R11 → P11 (Packet Loss Tinggi)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G14 (packet loss > 5%) | 0.9 | 0.0 | **0.9** |
| G23 (intermittent) | 0.5 | 0.3 | **0.2** |

### R12 → P12 (Latensi Tinggi)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G15 (ping > 100ms) | 0.9 | 0.0 | **0.9** |

### R13 → P13 (Firewall Memblokir)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G16 (aplikasi tertentu gagal) | 0.7 | 0.2 | **0.5** |
| G25 (firewall memblokir) | 0.9 | 0.0 | **0.9** |

### R14 → P14 (Kerusakan Kabel)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G18 (link lamp mati/berkedip) | 0.7 | 0.2 | **0.5** |
| G29 (kabel rusak/longgar) | 0.9 | 0.0 | **0.9** |
| G14 (packet loss > 5%) | 0.5 | 0.3 | **0.2** |

### R15 → P15 (Kerusakan Router/Switch)

| Symptom | MB | MD | CF Rule |
|---|---|---|---|
| G19 (semua client terdampak) | 0.9 | 0.0 | **0.9** |
| G27 (normal setelah restart) | 0.8 | 0.1 | **0.7** |
| G34 (router tidak respond) | 0.9 | 0.0 | **0.9** |

---

## 6. Ringkasan Statistik CF

| Metrik | Nilai |
|---|---|
| Jumlah total pasangan MB/MD | 36 |
| CF Rule tertinggi | **1.0** (G06 pada R06) |
| CF Rule terendah | **0.2** (G23 pada R11, G14 pada R14) |
| Range MB | 0.5 – 1.0 |
| Range MD | 0.0 – 0.3 |
| Gejala "deterministic" (MD=0.0) | 16 dari 36 |
| Rata-rata CF Rule | ≈ 0.71 |

### Distribusi CF Rule

| Rentang CF | Jumlah pasangan | Label (dari `interpret_cf`) |
|---|---|---|
| ≥ 0.80 | 16 | Sangat Yakin |
| 0.60 – 0.79 | 8 | Cukup Yakin |
| 0.40 – 0.59 | 8 | Kemungkinan |
| 0.20 – 0.39 | 4 | Kurang Yakin |
| < 0.20 | 0 | — |

---

## 7. Gejala Cross-Cutting (Muncul di Multiple Rule)

| Gejala | Dipakai di Rule | Penyakit Kandidat |
|---|---|---|
| G14 (packet loss > 5%) | R11, R14 | P11, P14 |
| G23 (intermittent) | R06, R11 | P06, P11 |
| G24 (akses via IP saja) | R03, R04 | P03, P04 |

**Konsekuensi:** Diagnosis bisa menghasilkan beberapa kandidat penyakit paralel (top-3), dan pemilihan gejala tambahan akan menentukan rule mana yang unggul. Kasus P11 vs P14 menjadi ujian ketat — keduanya sama-sama butuh G14; pembedanya adalah gejala pendamping (G23 → P11, atau G18+G29 → P14).

---

## 8. Gejala Orphan (Tidak Terpakai di Rule Manapun)

| Gejala | Nama | Catatan / Relevansi |
|---|---|---|
| G31 | VPN tidak bisa connect | Bisa jadi rule baru (VPN Misconfiguration) |
| G32 | VPN connect, internal tidak bisa diakses | Indikator split-tunnel / routing VPN |
| G33 | Lampu LAN di router mati | Berbeda dari G28 (WAN) dan G18 (NIC) |
| G36 | Network adapter disabled | Relevan ke P01, kandidat tambahan untuk R01 |
| G37 | Driver adapter bermasalah | Relevan ke P01 |
| G38 | Hanya satu perangkat bermasalah | Relevan ke P01 / P06 |
| G39 | Proxy setting aktif | Bisa jadi rule baru (Proxy Misconfiguration) |

**7 dari 40 gejala (17.5%) bersifat "dead knowledge"** — sudah didefinisikan di `symptoms.json` tapi tidak masuk ke `rules.json`. User bisa memilih gejala ini di form diagnosa, namun tidak akan mempengaruhi hasil diagnosis.

---

## 9. Algoritma Forward Chaining + CF

### Pseudocode (berdasar `inference/engine.py:22-92`)

```
FOR each rule R in knowledge_base:
    IF symptom_set(R) ⊆ selected_symptoms:    # AND strict matching
        FOR each symptom s in R:
            cf_rule     = MB(s) − MD(s)
            cf_evidence = cf_user(s) × cf_rule
        cf_combined = cf_evidence_1
        FOR i = 2 to n:
            cf_combined = cf_combined + cf_evidence_i × (1 − cf_combined)
        add to results
SORT results DESC by cf_combined
RETURN top 3
```

### Tiga Rumus CF yang Diimplementasikan

| Tahap | Rumus | Lokasi Kode |
|---|---|---|
| 1. CF rule (keyakinan pakar) | `CF(H,E) = MB − MD` | `engine.py:10` |
| 2. CF evidence (user × pakar) | `CF_evidence = CF_user × CF(H,E)` | `engine.py:15` |
| 3. CF combine (akumulasi bertahap) | `CF_combine = CF₁ + CF₂ × (1 − CF₁)` | `engine.py:20` |

### Threshold Interpretasi (`engine.py:103-115`)

| Range CF Final | Label |
|---|---|
| ≥ 0.80 | Sangat Yakin |
| 0.60 – 0.79 | Cukup Yakin |
| 0.40 – 0.59 | Kemungkinan |
| 0.20 – 0.39 | Kurang Yakin |
| < 0.20 | Tidak Yakin |

---

## 10. Contoh Perhitungan Lengkap (R02 → P02)

**Input user:** `{G02: 0.8, G03: 1.0, G28: 0.6, ...}`

### Tahap 1 — Hitung CF Evidence per Gejala

| Symptom | MB | MD | CF Rule | CF User | CF Evidence |
|---|---|---|---|---|---|
| G02 | 0.8 | 0.1 | 0.7 | 0.8 | 0.7 × 0.8 = **0.560** |
| G03 | 0.9 | 0.1 | 0.8 | 1.0 | 0.8 × 1.0 = **0.800** |
| G28 | 0.9 | 0.1 | 0.8 | 0.6 | 0.8 × 0.6 = **0.480** |

### Tahap 2 — Combine Bertahap

| Step | CFₐ | CFᵦ | Rumus | Result |
|---|---|---|---|---|
| 1 | 0.560 | 0.800 | 0.560 + 0.800 × (1 − 0.560) | **0.9120** |
| 2 | 0.912 | 0.480 | 0.912 + 0.480 × (1 − 0.912) | **0.9542** |

### Tahap 3 — Output

- `cf_final = 0.9542` → **95.42%**
- `cf_label = "Sangat Yakin"` (karena ≥ 0.80)
- Diagnosis: **P02 — Koneksi Internet Terputus**

---

## 11. Catatan Observasi Teknis

### Hal yang Sudah Benar

1. **Separation of concerns** bersih — knowledge base (JSON) terpisah dari inference engine (Python).
2. **Explainability lengkap** — setiap diagnosis menyimpan `evidence_steps` dan `combine_steps`, cocok untuk expert system yang transparan.
3. **Clamping CF** di `app.py` (`max(-1.0, min(1.0, cf_val))`) mencegah input out-of-range.
4. **MD ≤ 0.3** di seluruh knowledge base, sehingga rumus combine single-branch tetap valid — tidak perlu cabang negatif.

### Potensi Issue / Improvement

1. **AND-strict matching** — rule tidak akan "fire" bila salah satu gejala kurang. R12 (P12) adalah satu-satunya rule dengan single symptom (G15); ini cukup rapuh karena hanya butuh user tidak memilih G15 untuk tidak pernah mendapatkan P12 sebagai kandidat.
2. **7 orphan symptoms** (lihat §8) — bisa di-refine dengan menambah rule baru atau menghapus gejala dari `symptoms.json`.
3. **3 gejala cross-cutting** (G14, G23, G24) memungkinkan beberapa penyakit muncul bersamaan di top-3; secara klinis ini realistis (comorbidity), tapi perlu diwaspadai agar UI tidak membingungkan user.
4. **Rata-rata CF ≈ 0.71** cenderung optimis. Karena formula combine selalu meningkat untuk CF positif, sebagian besar diagnosis yang "fire" akan otomatis masuk label "Sangat Yakin" / "Cukup Yakin".
5. **Rule-to-Problem 1:1** — tidak ada multi-rule yang menargetkan penyakit yang sama, sehingga tidak terjadi kombinasi antar-rule (cross-rule CF combination). Ini pilihan desain simplifikasi, bukan kelemahan teoretis.

---

## 12. Referensi Terkait

- **Analisis implementasi sebelumnya:** [analisis-cf-forward-chaining-v1.0.0-NetMedix.md](analisis-cf-forward-chaining-v1.0.0-NetMedix.md)
- **Teori Certainty Factor (riset):** [2026-04-23_certainty-factor.md](2026-04-23_certainty-factor.md)
- **Teori Sistem Pakar (riset):** [2026-04-09_sistem-pakar-expert-system.md](2026-04-09_sistem-pakar-expert-system.md)
- **Source code engine:** `04_TUGAS/NetMedix/inference/engine.py`
- **Knowledge base:** `04_TUGAS/NetMedix/data/{problems,symptoms,rules}.json`

---

*Dibuat: 2026-07-06 | AI Model: Claude (glm-5) | Status: inbox*
