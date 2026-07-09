---
created_at: 2026-07-09
version_target: "2.0.0"
project: "NetMedix"
topic: "Tabel CF_pakar Riset Multi-Source NetMedix v2.0.0"
tags: [expert-system, certainty-factor, cf-pakar, knowledge-base, riset, netmedix]
related_files:
  - "[Perencanaan v2.0.0](../perencanaan-rombak-v2.0.0-NetMedix.md)"
  - "[Desain teknis v2.0.0](../desain-teknis-v2.0.0-NetMedix.md)"
  - "[TODO v2.0.0](../todo-rombak-v2.0.0-NetMedix.md)"
  - "[Discussion log](../../../00_INBOX/2026-07-09_discussion-rombak-netmedix-pure-cf.md)"
  - "[Baseline KB v1.0.0](./2026-07-06_analisis-cf-forward-chaining-netmedix.md)"
status: "complete-phase-1"
methodology: "Opsi D — Skala Ordinal Frekuensi + Engineering Judgment Override"
ai_model: "Claude (glm-5)"
document_structure: "partitioned-2026-07-10"
parts_count: 5
total_lines_original: 2904
---

# Tabel CF_pakar Riset Multi-Source NetMedix v2.0.0

> **Primary source of truth** untuk nilai `cf_pakar` per gejala per penyakit. Setiap nilai diturunkan dari riset multi-source artikel jaringan komputer dengan metodologi Opsi D. Dokumen ini menjadi dasar migrasi `data/rules.json` v2 (Phase 2).
>
> **ℹ️ Dokumen ini dipecah menjadi 5 part** pada `./tabel-cf-pakar-parts/` untuk efisiensi token (file asli 2904 baris / 243KB). File index ini berisi metodologi + daftar penyakit + TOC; detail per penyakit ada di file part. Lihat section "Struktur Dokumen" di bawah.

---

## Executive Summary

Tabel ini menggantikan struktur MB/MD (v1.0.0) dengan **CF_pakar single value per gejala** yang langsung diturunkan dari sintesis riset multi-source. Pendekatan ini lebih jujur secara epistemologis — nilai keyakinan pakar diturunkan dari frekuensi penyebutan di sumber kredibel (Microsoft Learn, Cisco, GeeksforGeeks, Cloudflare, vendor resmi) dan disesuaikan dengan engineering judgment berbasis domain knowledge jaringan.

**Progress saat ini:** 15 dari 15 penyakit LENGKAP + Fase 1.C orphan resolution SELESAI + **Fase 1.D peer review konsistensi SELESAI** + **Fase 1.E tutorial bundling verification SELESAI** — Fase 1.A sample (P12, P15) + Fase 1.B produksi massal (P01–P11, P13, P14) + Fase 1.C resolve 5/7 orphan (G36, G37, G38, G39) ke rule existing dan 2/7 orphan permanen (G31, G32 VPN) + Fase 1.D final peer review (5/6 dimensi PASS sempurna, 1 dimensi COMPLIANT dengan 2 minor documentation gaps) + Fase 1.E audit 40 gejala (G39 struktur YAML diperbaiki, G31/G32 stub out-of-scope ditambahkan, format konsistensi PASS). Metodologi Opsi D VALIDATED di 1.A, konsisten di 1.B, terbukti work untuk orphan resolution di 1.C, terkonfirmasi konsisten di 1.D, dan konten tutorial lengkap di 1.E. Total gejala-rule mappings 42; total gejala unik dengan tutorial 40/40 (38 full + 2 stub). **Siap untuk Phase 2 (migrasi rules.json/symptoms.json v2 schema).**

---

## Metodologi — Opsi D (Hybrid)

### Step 1 — Skala Ordinal Frekuensi (Default)

Setiap gejala dievaluasi berdasar berapa banyak sumber kredibel (≥ 3 sumber riset per penyakit) yang menyebutkannya sebagai indikator problem tsb:

| Frekuensi Penyebutan | Skala | CF_pakar Default |
|---|---|---|
| Semua sumber sebut sebagai **primary/signature symptom** | Sangat tinggi | **0.9** |
| Mayoritas sumber sebut sebagai **common symptom** | Tinggi | **0.7** |
| Sebagian sumber sebut, **supporting evidence** | Sedang | **0.5** |
| Hanya 1 sumber atau disebut minor | Rendah | **0.3** |
| Edge case, disebut sekilas | Sangat rendah | **0.1** |

### Step 2 — Engineering Judgment Override

Domain knowledge dapat meng-override nilai default dengan justifikasi tertulis:

- **Naik** (mis. 0.7 → 0.85): gejala adalah **differentiator unik** antara problem ini vs problem lain.
- **Turun** (mis. 0.7 → 0.5): gejala **cross-cutting** yang bisa muncul di banyak problem berbeda.
- Override wajib dicatat di kolom `evidence`.

### Step 3 — Triangulasi Sumber

Setiap nilai CF_pakar harus didukung **minimal 2 sumber independen**. Jika hanya 1 sumber → nilai maksimal dibatasi 0.5 (penalti lemah).

### Step 4 — Peer Review Konsistensi

Review silang untuk gejala cross-cutting (G14, G23, G24, dst.) apakah konsisten di semua kemunculan. Dieksekusi di Fase 1.D.

---

## Daftar Sumber Referensi Umum

| Kategori | Domain | Kredibilitas |
|---|---|---|
| Vendor documentation | cisco.com, learn.microsoft.com, support.apple.com, netgear.com, juniper.net, tp-link.com, asus.com | Tinggi — official vendor |
| Network monitoring vendor | netally.com, auvik.com, netbeez.net, kentik.com, domotz.com, manageengine.com, zscaler.com | Tinggi — domain expertise |
| Tech community reference | geeksforgeeks.org, howtogeek.com, makeuseof.com, superuser.com, community.cisco.com | Sedang — community-curated |
| Diagnostic tooling vendor | pingplotter.com, speedtesthq.com, ipfyi.com, calmops.com | Sedang — domain-specific |

---

## Daftar Penyakit (P01–P15)

| Kode | Nama | Kategori | Status |
|---|---|---|---|
| **P01** | **Tidak Ada Koneksi Jaringan** | **Konektivitas Dasar** | **✅ done** |
| **P02** | **Koneksi Internet Terputus** | **Konektivitas Dasar** | **✅ done** |
| **P03** | **DNS Resolution Failure** | **DNS** | **✅ done** |
| **P04** | **DNS Cache Poisoning / Hijacking** | **DNS** | **✅ done** |
| **P05** | **DHCP Failure** | **DHCP & IP Config** | **✅ done** |
| **P06** | **IP Address Conflict** | **DHCP & IP Config** | **✅ done** |
| **P07** | **Subnet Mask / Default Gateway Salah** | **DHCP & IP Config** | **✅ done** |
| **P08** | **Tidak Bisa Connect ke WiFi** | **WiFi** | **✅ done** |
| **P09** | **WiFi Signal Lemah / Interferensi** | **WiFi** | **✅ done** |
| **P10** | **Jaringan Lambat / Bandwidth Saturation** | **Performa** | **✅ done** |
| **P11** | **Packet Loss Tinggi** | **Performa** | **✅ done** |
| **P12** | **Latensi Tinggi / Jitter** | **Performa** | **✅ done (sample)** |
| **P13** | **Firewall Memblokir Koneksi** | **Keamanan** | **✅ done** |
| **P14** | **Kerusakan Kabel / Konektor Jaringan** | **Hardware** | **✅ done** |
| **P15** | **Kerusakan / Misconfiguration Router-Switch** | **Hardware** | **✅ done (sample)** |

---

## Struktur Dokumen (Part Index)

> Dokumen ini dipecah menjadi 5 part di subfolder `./tabel-cf-pakar-parts/` agar dapat dibaca per-batch tanpa loading 243KB penuh. Setiap part bersih di-boundary-nya (mulai di `##` heading, akhir di `---` separator).

### Per-Penyakit Sections (Detail CF_pakar, Evidence, Tutorial Gejala)

| Part File | Coverage Penyakit | Lines (file asli) |
|---|---|---|
| [01-penyakit-P12-P15-P01.md](./tabel-cf-pakar-parts/01-penyakit-P12-P15-P01.md) | **P12** Latensi/Jitter (sample) + **P15** Router-Switch (sample) + **P01** Tidak Ada Koneksi | 96–807 |
| [02-penyakit-P02-P03-P04-P05.md](./tabel-cf-pakar-parts/02-penyakit-P02-P03-P04-P05.md) | **P02** Internet Terputus + **P03** DNS Failure + **P04** DNS Poisoning + **P05** DHCP | 808–1430 |
| [03-penyakit-P06-P07-P08-P09-P10.md](./tabel-cf-pakar-parts/03-penyakit-P06-P07-P08-P09-P10.md) | **P06** IP Conflict + **P07** Subnet/Gateway + **P08** WiFi Connect + **P09** WiFi Lemah + **P10** Lambat | 1431–1985 |
| [04-penyakit-P11-P13-P14-orphan-stubs.md](./tabel-cf-pakar-parts/04-penyakit-P11-P13-P14-orphan-stubs.md) | **P11** Packet Loss + **P13** Firewall + **P14** Kabel + Orphan Stubs **G31/G32** VPN | 1986–2377 |
| [05-reviews-fase-1C-1D-1E-tracking.md](./tabel-cf-pakar-parts/05-reviews-fase-1C-1D-1E-tracking.md) | Cross-Cutting Tracking + **Fase 1.C** Orphan Decisions + **Fase 1.D** Peer Review Final + **Fase 1.E** Tutorial Verification + Progress | 2378–2904 |

### Cara Membaca (Panduan Penggunaan)

| Kebutuhan | File yang dibaca |
|---|---|
| Memahami metodologi & daftar penyakit | File index ini saja (cukup) |
| Migrasi `rules.json` v2 (Phase 2 — CF_pakar + sources + evidence per penyakit) | Part **01 → 02 → 03 → 04** berurutan |
| Migrasi `symptoms.json` v2 (Phase 2 — tutorial per gejala) | Part **01 → 02 → 03 → 04** (tutorial embedded per penyakit) + orphan stubs di part 04 |
| Verifikasi konsistensi & peer review | Part **05** |
| Cek nilai spesifik satu penyakit | Lihat tabel part index di atas, buka part yg sesuai |

### Backup

- **File asli lengkap (sebelum split 2026-07-10)** tersimpan di git history — commit sebelum split (`64e29ad` - Fase 1.E) masih menyimpan `tabel-cf-pakar-riset.md` versi full 243KB / 2904 baris. Recovery via: `git show 64e29ad:docs-NetMedix/tabel-cf-pakar-riset.md`

### Catatan Split

- **Tanggal split:** 2026-07-10
- **Metode:** `sed -n 'START,ENDp'` per part — content tidak dimodifikasi, hanya di-slice
- **Verifikasi integritas:** 712 + 623 + 555 + 392 + 527 = 2809 baris di parts + 95 di index (sebelum penambahan TOC) = 2904 baris = file asli ✓
- **Referensi eksternal:** Link di `perencanaan-rombak-v2.0.0-NetMedix.md`, `desain-teknis-v2.0.0-NetMedix.md`, `todo-rombak-v2.0.0-NetMedix.md` tetap menunjuk ke file index ini (`tabel-cf-pakar-riset.md`) — tidak ada yang perlu diupdate karena filename tetap sama, hanya content yang di-slim

---

*Dibuat: 2026-07-09 | Updated: 2026-07-10 (partitioned into 5 parts + index untuk efisiensi token) | Methodology: Opsi D (skala ordinal + engineering judgment) | Status: Fase 1.A + 1.B + 1.C + 1.D + 1.E LENGKAP — 15/15 penyakit + 6/7 orphan resolved + 2/7 orphan permanen dengan stub + peer review final lulus + tutorial bundling verification lulus (40/40 gejala). Next: Phase 2 (migrasi rules.json/symptoms.json v2 schema).*
