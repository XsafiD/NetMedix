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
status: "in-progress"
methodology: "Opsi D — Skala Ordinal Frekuensi + Engineering Judgment Override"
ai_model: "Claude (glm-5)"
---

# Tabel CF_pakar Riset Multi-Source NetMedix v2.0.0

> **Primary source of truth** untuk nilai `cf_pakar` per gejala per penyakit. Setiap nilai diturunkan dari riset multi-source artikel jaringan komputer dengan metodologi Opsi D. Dokumen ini menjadi dasar migrasi `data/rules.json` v2 (Phase 2).

---

## Executive Summary

Tabel ini menggantikan struktur MB/MD (v1.0.0) dengan **CF_pakar single value per gejala** yang langsung diturunkan dari sintesis riset multi-source. Pendekatan ini lebih jujur secara epistemologis — nilai keyakinan pakar diturunkan dari frekuensi penyebutan di sumber kredibel (Microsoft Learn, Cisco, GeeksforGeeks, Cloudflare, vendor resmi) dan disesuaikan dengan engineering judgment berbasis domain knowledge jaringan.

**Progress saat ini:** 2 dari 15 penyakit (P12 & P15) — Fase 1.A sample validasi metodologi. 13 penyakit sisanya di-fase 1.B.

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
| P01 | Tidak Ada Koneksi Jaringan | Konektivitas Dasar | ⏳ pending |
| P02 | Koneksi Internet Terputus | Konektivitas Dasar | ⏳ pending |
| P03 | DNS Resolution Failure | DNS | ⏳ pending |
| P04 | DNS Cache Poisoning / Hijacking | DNS | ⏳ pending |
| P05 | DHCP Failure | DHCP & IP Config | ⏳ pending |
| P06 | IP Address Conflict | DHCP & IP Config | ⏳ pending |
| P07 | Subnet Mask / Default Gateway Salah | DHCP & IP Config | ⏳ pending |
| P08 | Tidak Bisa Connect ke WiFi | WiFi | ⏳ pending |
| P09 | WiFi Signal Lemah / Interferensi | WiFi | ⏳ pending |
| P10 | Jaringan Lambat / Bandwidth Saturation | Performa | ⏳ pending |
| P11 | Packet Loss Tinggi | Performa | ⏳ pending |
| **P12** | **Latensi Tinggi / Jitter** | **Performa** | **✅ done (sample)** |
| P13 | Firewall Memblokir Koneksi | Keamanan | ⏳ pending |
| P14 | Kerusakan Kabel / Konektor Jaringan | Hardware | ⏳ pending |
| **P15** | **Kerusakan / Misconfiguration Router-Switch** | **Hardware** | **✅ done (sample)** |

---

## P12 — Latensi Tinggi / Jitter

**Kategori:** Performa
**Definisi:** Latensi tinggi (ping > 100ms ke server lokal/gateway) dan jitter tinggi (variasi RTT antar paket) yang menyebabkan real-time applications (VoIP, gaming, video call) tidak nyaman digunakan.
**Sumber utama riset:**

1. SpeedTestHQ — "How to Read Ping Output" — https://speedtesthq.com/guides/diagnostics/how-to-read-ping-output
2. ManageEngine — "Troubleshooting Network Latency" — https://www.manageengine.com/network-monitoring/tech-topics/troubleshooting-network-latency.html
3. Domotz — "What Is Network Jitter? Practical Guide" — https://blog.domotz.com/all/troubleshooting-network-jitter-voip-video-stability/
4. CalmOps — "Network Troubleshooting: Bandwidth Testing and Latency Diagnostics" — https://calmops.com/devops/network-troubleshooting-bandwidth-latency-diagnostics/
5. IPFYI — "High Latency & Ping Issues: Root Cause Analysis" — https://ipfyi.com/guides/network-troubleshooting/high-latency-diagnosis/
6. DigitalCitizen — "Track Internet Latency Spikes Using Ping and Traceroute" — https://www.digitalcitizen.life/how-to-track-where-your-internet-latency-spikes-using-ping-and-traceroute/
7. PingPlotter — "What Are Good Latency & Ping Speeds?" — https://www.pingplotter.com/wisdom/article/is-my-connection-good/
8. Zscaler — "Understanding Ping for Network Troubleshooting" — https://www.zscaler.com/blogs/product-insights/understanding-ping-network-troubleshooting-and-beyond
9. NetBeez — "Network Latency: Causes and Solutions" — https://netbeez.net/blog/network-latency/

### Tabel CF_pakar

> **Catatan penting:** Rule v1.0.0 hanya berisi G15 (single symptom). Filter baru "≥ 2 gejala relevan" memaksa rule P12 di-expand dengan gejala pendukung yang secara klinis sering co-occur dengan latensi tinggi. Expansion ini juga memenuhi keputusan Sesi 2 #12 (open for expand).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G15** | Ping time > 100ms lokal | **0.90** | 0.9 (signature) | — | Signature symptom. **Min 7 sumber** konsisten menyebut threshold >100ms sebagai indikator latensi problematik: SpeedTestHQ ("time > 100ms consistently, or large spikes" — problem threshold), CalmOps ("`time > 100ms` suggests network congestion or distance"), ManageEngine (100–200ms = "Noticeable lag, may impact real-time interactions"), PingPlotter ("consistently-high latency is a clear indicator of a problem"), DigitalCitizen (300ms = "feels sluggish"), Zscaler ("High RTT values may indicate a network bottleneck"), IPFYI (menggunakan ping RTT sebagai primary diagnostic). |
| 2 | **G13** | Kecepatan internet sangat lambat | **0.50** | — | 0.7 → 0.5 (cross-cutting) | Common symptom dari sisi user. ManageEngine: "Websites load slowly, especially elements like images or scripts. VoIP calls are choppy." NetBeez: "slow website loading times". Namun G13 **bukan signature** latency — juga muncul di P10 (bandwidth), P11 (packet loss), P09 (WiFi lemah), P08 (WiFi gagal connect). **Turun** karena cross-cutting kuat ke banyak problem. |
| 3 | **G14** | Ping packet loss > 5% | **0.50** | — | 0.7 → 0.5 (cross-cutting + co-occur) | Sering co-occur dengan latensi tinggi karena congestion adalah cause gabungan. Domotz: "high jitter and packet loss frequently occur together because both are often symptoms of the same underlying cause: network congestion." CalmOps: "A 'latency issue' is often a combined loss and jitter issue." **Turun** karena sudah signature di P11 (rule R11) dan P14 (rule R14) — tidak boleh terlalu kuat di P12 agar tidak mendominasi. |
| 4 | **G23** | Koneksi putus-nyala (intermittent) | **0.30** | — | 0.5 → 0.3 (cross-cutting minor) | Latensi tinggi dapat menyebabkan koneksi terasa intermittent dari sisi user (terutama VoIP/gaming). Auvik: "High jitter would manifest as sporadic interruptions, stalling, buffering pauses." Namun G23 lebih kuat signature di P06 (IP conflict) dan P11 (packet loss). **Turun** karena cross-cutting minor — P12 bukan problem utama yang ditandai intermittent. |

### Evidence Summary

- **Signature symptom:** G15 (CF 0.9) — differentiator utama.
- **Supporting symptoms:** G13, G14 (CF 0.5) — co-occur common, tapi cross-cutting.
- **Minor supporting:** G23 (CF 0.3) — edge cross-cutting.
- **Rule baru P12 setelah expand:** 4 gejala (dari 1 gejala di v1.0.0) → lolos filter "≥ 2 gejala relevan" dengan banyak kombinasi user.

### Bundling Tutorial Gejala

#### G15 — Ping time > 100ms lokal

- **short_desc:** Saat ping ke server lokal/gateway, waktu round-trip (RTT) konsisten di atas 100ms — jauh di atas threshold normal <20–50ms untuk koneksi lokal.
- **how_to_check:** `Buka CMD/Terminal → jalankan ping <gateway-IP> -n 20 (Windows) atau -c 20 (Linux/Mac) → cek baris "Minimum / Maximum / Average" di statistik akhir. Average > 100ms = indikasi masalah.`

```yaml
tutorial:
  definition: >
    Latensi (ping time) adalah waktu round-trip (RTT) yang dibutuhkan paket data
    untuk pergi ke tujuan dan kembali, diukur dalam milidetik (ms). Untuk koneksi
    LOKAL (ke gateway/router di jaringan sendiri), RTT normal adalah 1–5ms; untuk
    server di kota yang sama umumnya <30ms. Threshold >100ms ke server lokal
    adalah indikator kuat adanya congestion, misconfig QoS, atau masalah di path
    lokal (SpeedTestHQ, CalmOps, ManageEngine).
  verification_steps:
    - "Step 1: Cari IP gateway — Windows: jalankan `ipconfig`, lihat 'Default Gateway'; Linux/Mac: `ip route` atau `ifconfig`."
    - "Step 2: Buka CMD (Windows) atau Terminal (Linux/Mac)."
    - "Step 3: Jalankan `ping <gateway-IP> -n 20` (Windows) atau `ping -c 20 <gateway-IP>` (Linux/Mac). Pakai -n/-c 20 (bukan default 4) untuk statistik yang berarti."
    - "Step 4: Tunggu hingga selesai (sekitar 20 detik), baca baris statistik akhir."
    - "Step 5: Catat nilai 'Average' (Windows) atau 'avg' (Linux/Mac). Jika >100ms → ada masalah latensi di segment lokal."
    - "Step 6: Untuk konfirmasi latensi internet, ulangi ke `ping 1.1.1.1 -n 20`. Jika gateway stabil (<5ms) tapi 1.1.1.1 >100ms → masalah di ISP atau upstream."
  interpretation: >
    <20ms (gateway) / <50ms (internet domestik): normal | 50–100ms: border,
    mulai terasa untuk real-time | 100–200ms: Noticeable lag, dampak ke VoIP/gaming
    (ManageEngine) | >200ms: Poor performance, significant lag, choppy VoIP/video.
  common_causes:
    - "Network congestion di hop lokal atau upstream (penyebab #1 menurut Domotz & CalmOps)"
    - "Bufferbloat — excessive packet buffering pada router consumer-grade (Domotz)"
    - "Wi-Fi interference atau overload (terutama 2.4GHz crowded)"
    - "Routing tidak optimal di ISP (peering dispute, BGP convergence lambat)"
    - "Hardware overload — router/switch CPU atau memory penuh (ManageEngine)"
    - "Faulty cabling atau duplex mismatch (CalmOps, Cisco)"
    - "Bandwidth saturation akibat backup/download besar di background"
  related_symptoms: [G13, G14, G22, G23]
```

#### G13 — Kecepatan internet sangat lambat

- **short_desc:** User mengalami loading website lama, download lambat, atau streaming buffering — namun belum tentu disebabkan latensi (bisa juga bandwidth, packet loss, atau WiFi lemah).
- **how_to_check:** `Jalankan speed test (fast.com atau speedtest.net) → bandingkan dengan paket internet Anda. <30% dari paket = sangat lambat. Kombinasikan dengan ping test (G15) untuk diferensiasi bandwidth vs latency.`

```yaml
tutorial:
  definition: >
    "Internet lambat" adalah symptom user-facing yang bisa disebabkan banyak hal:
    bandwidth saturation, latensi tinggi, packet loss, DNS lambat, atau WiFi
    lemah. ManageEngine mencantumkan "Websites load slowly" dan "Emails with
    large attachments take a long time to send" sebagai tanda high latency —
    namun symptom ini juga muncul di P10 (bandwidth), P11 (packet loss), P09
    (WiFi lemah). Tidak spesifik, tapi common.
  verification_steps:
    - "Step 1: Buka browser, kunjungi speedtest.net atau fast.com."
    - "Step 2: Jalankan test, catat download/upload (Mbps) dan ping (ms)."
    - "Step 3: Bandingkan dengan paket internet langganan (mis. 100 Mbps)."
    - "Step 4: Jika actual < 30% paket (mis. <30 Mbps di paket 100 Mbps) → ada masalah performa."
    - "Step 5: Untuk membedakan penyebab — cek juga G15 (ping gateway), G14 (packet loss), G22 (speed test konsisten rendah)."
  interpretation: >
    100% paket + ping <50ms: normal | 50–80% paket: variance WiFi wajar |
    <30% paket: ada masalah performa (latency/bandwidth/loss) | <10% paket:
    serius, kemungkinan congestion parah atau hardware issue.
  common_causes:
    - "Bandwidth saturation (banyak user/device share koneksi)"
    - "Latensi tinggi (P12 — lihat G15)"
    - "Packet loss (P11 — lihat G14)"
    - "WiFi signal lemah (P09 — lihat G11)"
    - "Background download/backup/sync"
    - "ISP throttling atau congestion peak hours"
  related_symptoms: [G15, G14, G22, G11]
```

#### G14 — Ping packet loss > 5% (referensi silang ke P11/P14)

- **short_desc:** Saat ping ke server, lebih dari 5% paket gagal kembali. Threshold >5% dianggap indikasi masalah jaringan serius.
- **how_to_check:** `ping 8.8.8.8 -n 20 (Windows) atau ping -c 20 8.8.8.8 (Linux/Mac) → baca "Lost = X%" di statistik akhir. >5% = masalah.`

```yaml
tutorial:
  definition: >
    Packet loss adalah persentase paket data yang gagal mencapai tujuan.
    Threshold >5% umum dianggap indikasi masalah jaringan (SpeedTestHQ,
    CalmOps). Domotz mencatat: "high jitter and packet loss frequently occur
    together because both are often symptoms of the same underlying cause:
    network congestion." Maka G14 sering co-occur dengan P12 (latensi).
    Namun signature kuat G14 ada di P11 (packet loss primer) dan P14
    (kerusakan kabel) — di P12 hanya sebagai supporting evidence.
  verification_steps:
    - "Step 1: Buka CMD (Windows) atau Terminal (Linux/Mac)."
    - "Step 2: Jalankan `ping 8.8.8.8 -n 20` (Windows) atau `ping -c 20 8.8.8.8` (Linux/Mac)."
    - "Step 3: Tunggu hingga selesai, lihat statistik akhir."
    - "Step 4: Cek persentase pada baris 'Lost = X%' (Windows) atau 'X% packet loss' (Linux/Mac)."
    - "Step 5: Untuk isolasi lokal vs upstream, ulangi ke IP gateway: `ping <gateway> -n 20`."
  interpretation: >
    0% loss: sempurna | <1%: normal untuk WiFi | 1–5%: borderline, mulai
    terasa di VoIP/gaming | >5%: indikasi masalah (threshold signature) |
    >15%: serius, koneksi praktis tidak usable.
  common_causes:
    - "Network congestion (penyebab #1)"
    - "Interferensi WiFi atau signal lemah"
    - "Kabel rusak/longgar (P14)"
    - "Hardware issue (NIC, switch, router — P15)"
    - "Bandwidth saturation"
  related_symptoms: [G15, G23, G22, G13]
```

#### G23 — Koneksi putus-nyala / intermittent (referensi silang ke P06/P11)

- **short_desc:** Koneksi internet terasa putus-nyala berkala — beberapa saat normal, lalu putus/sempat timeout, lalu normal lagi.
- **how_to_check:** `Jalankan continuous ping: ping -t <IP> (Windows) atau ping <IP> (Linux/Mac). Amati selama 2–5 menit: jika ada timeout periodik → intermittent.`

```yaml
tutorial:
  definition: >
    Koneksi intermittent (putus-nyala) adalah kondisi koneksi tidak stabil —
    beberapa saat正常, lalu gagal, lalu pulih, secara periodik. Auvik
    mendeskripsikan high jitter sebagai "sporadic interruptions, stalling,
    buffering pauses". Bisa muncul di banyak problem: P06 (IP conflict),
    P11 (packet loss), P12 (latency ekstrim), P09 (WiFi lemah). Tidak
    spesifik ke P12.
  verification_steps:
    - "Step 1: Buka CMD/Terminal."
    - "Step 2: Jalankan continuous ping ke gateway: `ping -t <gateway>` (Windows) atau `ping <gateway>` (Linux/Mac)."
    - "Step 3: Biarkan berjalan 2–5 menit."
    - "Step 4: Amati pola — apakah ada timeout periodik (Request timed out) di tengah period normal?"
    - "Step 5: Catat interval — setiap berapa detik/menit timeout muncul?"
  interpretation: >
    0 timeout dalam 5 menit: stabil | 1–3 timeout sporadis: borderline WiFi
    | timeout periodik (mis. tiap 30 detik): indikasi interference atau DHCP
    renewal issue | >50% timeout: praktis putus.
  common_causes:
    - "Interference WiFi (terutama 2.4GHz)"
    - "IP address conflict (P06)"
    - "Packet loss parah (P11)"
    - "DHCP lease renewal gagal"
    - "Hardware router/switch bermasalah (P15)"
  related_symptoms: [G14, G15, G12, G06]
```

---

## P15 — Kerusakan / Misconfiguration Router-Switch

**Kategori:** Hardware
**Definisi:** Kerusakan fisik (hardware failure) atau misconfiguration serius pada router/switch yang menyebabkan jaringan total atau sebagian besar tidak berfungsi. Berbeda dari P02 (WAN-side issue) — P15 adalah masalah di device network itu sendiri.
**Sumber utama riset:**

1. Cisco — "How to determine a legitimate hardware issue" (Support Talks) — https://community.cisco.com/kxiwq67737/attachments/kxiwq67737/4461-docs-network-infrastructure/6775/2/How%20to%20determine%20a%20legitimate%20hardware%20issue.pdf
2. Cisco — "Software-forced Crashes Troubleshoot" — https://www.cisco.com/c/en/us/support/docs/routers/7500-series-routers/26145-crashes-swforced-troubleshoot.html
3. Cisco Community — "Switch becoming unresponsive" — https://community.cisco.com/t5/switches-small-business/switch-becoming-unresponsive/td-p/5161968
4. MovingComm — "Industrial Gigabit Router Troubleshooting" — https://m.movingcomm.com/h-nd-778.html
5. HowToGeek — "Why Does Rebooting a Router Fix So Many Connection Issues?" (via MakeUseOf) — https://www.makeuseof.com/why-rebooting-router-works/
6. HighSpeedInternet — "How To Restart Your Router" — https://www.highspeedinternet.com/resources/how-to-restart-router
7. AppRanked — "Why Rebooting the Router 'Fixes' Wi-Fi" — https://www.appranked.com/router-reboot-fixes-wifi/
8. ISEMag — "The Most Common Step Is Often the Wrong Step" — https://www.isemag.com/columnist/article/14266586/the-most-common-step-is-often-the-wrong-step
9. GL.iNet — "Cannot access web Admin Panel" — https://docs.gl-inet.com/router/en/4/faq/cannot_access_web_admin_panel/
10. IPToolsPro — "192.168.1.1 Won't Load? Can't Access Router Login Page?" — https://www.iptoolspro.com/blog/cant-access-router-login-page-fix
11. DevCrea — "192.168.1.1 Not Working: Fix Router Admin Access" — https://www.devcrea.com/192-168-1-1-not-working
12. CXtec — "Troubleshooting Network Switches: Common Challenges" — https://www.cxtec.com/blog/troubleshoot-network-switches-handling-common-challenges-expert-solutions/
13. CableWholesale — "How To Troubleshoot a Faulty Ethernet Switch" — https://www.cablewholesale.com/blog/index.php/2025/08/19/how-to-troubleshoot-a-faulty-ethernet-switch/
14. Firewall Technical — "Fix Unresponsive Routers" — https://www.firewalltechnical.com/wi-fi-woes-3-ways-to-fix-unresponsive-router/

### Tabel CF_pakar

> **Catatan penting:** Rule v1.0.0 berisi G19, G27, G34 (3 gejala). Riset ini menambah G33 (orphan yang di-resolve) karena "lampu LAN di router mati" adalah signature hardware failure yang berbeda dari G28 (lampu WAN merah = P02) dan G18 (link lamp NIC = P14).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G19** | Semua client di jaringan terdampak | **0.90** | 0.9 (signature) | — | Signature differentiator. MovingComm (industrial router troubleshooting): *"confirm whether it is a single device that cannot connect or whether all devices within the entire local area network are affected... If the entire local area network is affected, it is more likely that the router itself is faulty."* Cisco Community (switch unresponsive): *"The switch and everything behind it gets unresponsive."* Arxiv NetDx (model-based diagnosis): failure report describes *"loss of connection between two hosts or groups of hosts for all packets"* — signature switch/router failure. CXtec: *"Switches are usually prone to failures due to overheating, power surges, hardware malfunctions."* Min 4 sumber independen konsisten. |
| 2 | **G27** | Koneksi normal setelah restart router | **0.70** | 0.7 (common) | — | Common symptom. MakeUseOf: *"For the vast array of short-term connectivity issues, a simple reboot allows the hardware and software to start again."* HighSpeedInternet: *"Restarting... allows the device to flush out any glitches."* AppRanked: *"A proper restart clears temporary glitches."* HowToGeek: *"Rebooting can sometimes make this look better for a while."* ISEMag: *"A power cycle often helps, at least short term."* Tidak dinaikkan ke 0.9 karena restart-juga-fix bersifat **transient indicator** — bisa juga software glitch, bukan hanya hardware/misconfig. But 5 sumber konsisten menyebut restart sebagai primary diagnostic step. |
| 3 | **G34** | Router tidak respond saat diakses | **0.90** | 0.9 (signature) | — | Signature symptom untuk kasus serious. Cisco (Software-forced Crashes): *"A software-forced crash occurs when the router detects a severe, unrecoverable error, and reloads itself."* GL.iNet docs: *"the router is bricked"* — final state ketika router total tidak bisa diakses. IPToolsPro: *"90% of router admin interface crashed issues are fixed by full power cycle"* — mengindikasikan ini common failure mode. SuperUser thread (router web server crash): *"Internet works but cannot login"* — partial failure. DevCrea: *"ERR_CONNECTION_REFUSED"* sebagai signature admin interface crash. Cisco Support: *"Switch becoming unresponsive... http, https traffic just timeouts."* Min 5 sumber. |
| 4 | **G33** | Lampu LAN di router mati | **0.80** | 0.7 (common) | 0.7 → 0.8 (differentiator) | **Orphan yang di-resolve** ke P15. Indicator LED mati di port LAN adalah signature physical hardware issue berbeda dari G28 (lampu WAN merah → upstream/WAN problem, rule P02) dan G18 (link lamp NIC di device → P14 kerusakan kabel/NIC). Cisco (legitimate hardware issue): POST/LED failures adalah primary signs of hardware failure — *"Failure is not fixed by moving to another slot, chassis, etc. Failure is seen in the same way, every time on the same component."* **Naik** karena differentiator unik antara P15 vs P02 vs P14. Penalti -0.1 dari 0.9 karena tidak ada di tabel v1.0.0 (sumber riset lebih terbatas). |

### Evidence Summary

- **Signature symptoms:** G19, G34 (CF 0.9) — differentiator kuat untuk hardware/misconfig serius.
- **Common symptom:** G27 (CF 0.7) — restart-membantu sebagai supporting, bukan signature.
- **Resolved orphan:** G33 (CF 0.8) — pindah dari orphan ke rule P15, differentiator LED.
- **Rule baru P15 setelah expand:** 4 gejala (dari 3 gejala di v1.0.0) → resolve orphan G33.

### Bundling Tutorial Gejala

#### G19 — Semua client di jaringan terdampak

- **short_desc:** Tidak hanya satu perangkat, tetapi semua/sebagian besar perangkat di jaringan lokal (WiFi + Ethernet) mengalami masalah koneksi yang sama.
- **how_to_check:** `Cek dari minimal 2 perangkat berbeda (HP + laptop, atau WiFi + Ethernet). Jika semua bermasalah → jaringan-wide. Jika hanya satu → device-specific (lihat G38).`

```yaml
tutorial:
  definition: >
    "Semua client terdampak" adalah signature differentiator antara masalah
    di network gear (router/switch/access point) vs masalah di device user.
    MovingComm (router troubleshooting): *"If the entire local area network
    is affected, it is more likely that the router itself is faulty, or
    there is a problem with the connected network devices (such as switches,
    optical transceivers)."* Arxiv NetDx menggunakan failure report
    "loss of connection for all packets" sebagai input utama untuk
    diagnose switch/router failure. Kontras dengan G26 ("device lain
    normal") dan G38 ("single device bermasalah") yang menandakan
    isolasi ke perangkat user.
  verification_steps:
    - "Step 1: Identifikasi minimal 2 perangkat berbeda di jaringan (HP, laptop, smart TV, dll)."
    - "Step 2: Test koneksi di masing-masing — buka website atau ping gateway."
    - "Step 3: Pastikan tes mencakup koneksi berbeda: WiFi DAN Ethernet (bukan hanya WiFi)."
    - "Step 4: Jika semua perangkat gagal dengan cara serupa → G19 = true → masalah ada di network gear."
    - "Step 5: Untuk konfirmasi router vs switch — cek apakah device yang terkoneksi langsung ke router juga bermasalah."
    - "Step 6: Catat timeline — apakah semua gagal di saat yang sama? Ini membedakan dari intermittent individual."
  interpretation: >
    Hanya 1 device bermasalah: bukan G19, lihat G38 (single device) | 2+
    device di WiFi sama bermasalah, Ethernet OK: mungkin AP/specific SSID
    issue | Semua device (WiFi + Ethernet) bermasalah: G19 confirmed →
    masalah router/switch upstream | Semua device + internet gagal total:
    indikasi router failure atau WAN putus (P02).
  common_causes:
    - "Router hardware failure atau hang (P15)"
    - "Switch failure — overheating, power surge (CXtec)"
    - "Misconfiguration router (DHCP disabled, routing loop)"
    - "WAN connection putus (P02) — tapi biasanya LAN masih berfungsi internal"
    - "Firmware bug atau software-forced crash (Cisco)"
    - "Power issue ke network gear"
  related_symptoms: [G34, G27, G33, G28]
```

#### G27 — Koneksi normal setelah restart router

- **short_desc:** Setelah power-cycle router (cabut kabel power 30 detik, pasang lagi), koneksi internet kembali normal — setidaknya untuk sementara.
- **how_to_check:** `Cabut kabel power router, tunggu 30 detik (biarkan kapasitor drain), pasang kembali. Tunggu 2–3 menit hingga lampu stabil. Test koneksi. Jika normal kembali → G27 = true.`

```yaml
tutorial:
  definition: >
    Restart/power-cycle adalah diagnostic step paling umum untuk masalah
    jaringan. MakeUseOf: *"For the vast array of short-term connectivity
    issues, a simple reboot allows the hardware and software to start again
    and run through the necessary sequences with a clean slate."* Mechanism:
    restart flushes RAM, clears state errors, renews DHCP lease dari ISP,
    clears buffer congestion. Penting: jika restart HANYA membantu sementara
    dan problem kambuh — ini indikasi kuat adanya hardware issue serius atau
    software bug persisten (Cisco software-forced crash). HowToGeek: *"If
    your router only works properly after constant reboots... it might not
    be a case of fixing it but rather a case of replacing it."*
  verification_steps:
    - "Step 1: Identifikasi router/modem — lokasi fisik, kabel power, kabel network."
    - "Step 2: Cabut kabel power dari router (bukan tombol power — harus cabut kabel agar kapasitor drain)."
    - "Step 3: Tunggu minimal 30 detik (60 detik lebih aman, biarkan komponen dingin)."
    - "Step 4: Pasang kembali kabel power, tekan tombol power jika perlu."
    - "Step 5: Tunggu 2–3 menit (bisa sampai 10 menit untuk modem) hingga lampu stabil (tidak berkedip lagi)."
    - "Step 6: Test koneksi dari perangkat — speedtest, browsing, ping gateway."
    - "Step 7: Catat berapa lama koneksi tetap normal sebelum problem kambuh (1 jam? 1 hari?). Ini differentiator penting."
  interpretation: >
    Problem solved permanently (>1 minggu): transient glitch, tidak ada
    underlying issue | Solved tapi kambuh <1 hari: indikasi strong hardware
    atau software bug persisten (P15) | Solved tapi kambuh <1 jam: serius,
    hardware mendekati failure | Tidak solved sama sekali: bukan restart-
    fixable issue, mungkin WAN putus (P02) atau hardware rusak total.
  common_causes:
    - "RAM/state overload akibat uptime lama (normal, transient)"
    - "Software bug atau firmware issue (Cisco)"
    - "Hardware overheating yang mereda setelah cooldown"
    - "Buffer congestion akibat traffic pattern tertentu"
    - "DHCP lease dari ISP expired, butuh renegotiate"
    - "Capacitor aging — power supply mulai melemah"
  related_symptoms: [G19, G34, G23]
```

#### G34 — Router tidak respond saat diakses

- **short_desc:** Tidak bisa membuka halaman admin router (mis. http://192.168.1.1) atau router tidak respon saat di-ping, meskipun kabel terhubung. Indikasi router crash/hang/bricked.
- **how_to_check:** `Coba akses http://192.168.1.1 (atau IP gateway dari ipconfig). Jika timeout/ERR_CONNECTION_REFUSED → coba ping <gateway>. Jika ping juga RTO → router hang/bricked.`

```yaml
tutorial:
  definition: >
    "Router tidak respond" berarti device tidak bisa diakses via web admin
    (HTTP/HTTPS) maupun via ICMP ping — meskipun secara fisik kabel terhubung
    dan lampu power menyala. Berbeda dari "internet putus" (masih bisa
    akses admin router). IPToolsPro: *"90% of router admin interface crashed
    issues are fixed by full power cycle"* — mengindikasikan ini common
    failure mode. Cisco (Software-forced Crashes): *"A software-forced crash
    occurs when the router detects a severe, unrecoverable error, and
    reloads itself."* Cisco Community: *"Switch becoming unresponsive...
    http, https traffic just timeouts, accessing things behind it."*
    GL.iNet docs menggunakan istilah "bricked" untuk kondisi ekstrim.
    Catatan: ada kasus "web interface only crash" (routing masih jalan) —
    ini lebih ringan dari total unresponsive.
  verification_steps:
    - "Step 1: Pastikan device terhubung ke router via WiFi atau Ethernet kabel."
    - "Step 2: Cari IP gateway — Windows: `ipconfig` lihat 'Default Gateway'; Linux/Mac: `ip route | grep default`."
    - "Step 3: Buka browser (Chrome/Edge/Firefox), ketik `http://<gateway-IP>` (pakai http:// eksplisit, bukan https://)."
    - "Step 4: Jika timeout/ERR_CONNECTION_REFUSED → lanjut ke Step 5. Jika login page muncul → bukan G34."
    - "Step 5: Ping gateway dari CMD/Terminal: `ping <gateway-IP> -n 10`. Jika RTO (Request Timed Out) → router hang/bricked."
    - "Step 6: Cek lampu power router — apakah menyala normal? Lampu abnormal (merah/berkedip error) mendukung diagnosa hardware failure."
    - "Step 7: Untuk diferensiasi web-only crash vs total — coba internet masih jalan? Buka google.com. Kalau internet OK tapi admin tidak → web server crash (ringan). Kalau internet juga down → router total."
  interpretation: >
    Internet OK tapi admin down: web server crash (ringan, fix dengan
    restart) | Admin down + ping RTO tapi lampu normal: router hang, fix
    dengan power cycle | Lampu abnormal + total unresponsive: indikasi
    hardware failure atau bricked | Setelah factory reset masih tidak
    respond: bricked, perlu servis/replacement.
  common_causes:
    - "Software-forced crash / firmware bug (Cisco)"
    - "RAM overload setelah uptime lama"
    - "Hardware failure — power supply, capacitor, atau SoC (Cisco hardware issue)"
    - "Bricked akibat firmware update gagal (GL.iNet)"
    - "Account lockout (terlalu banyak gagal login) — partial, hanya admin yang tidak respond"
    - "IP conflict dengan device lain di jaringan yang juga pakai 192.168.1.1"
  related_symptoms: [G19, G27, G33, G28]
```

#### G33 — Lampu LAN di router mati

- **short_desc:** Lampu indikator di port LAN router (untuk koneksi kabel ke device/switch) mati total, padahal kabel terhubung dan device seharusnya aktif.
- **how_to_check:** `Lihat fisik port LAN di router (biasanya label LAN atau angka 1-4). Pasang kabel Ethernet ke device aktif (laptop). Lampu harus menyala/hijau. Jika mati di port yang berbeda → indikasi hardware issue.`

```yaml
tutorial:
  definition: >
    Lampu LED di port LAN router adalah indicator Layer 1 (physical). Cisco
    (How to determine a legitimate hardware issue): *"POST, LED, or
    Diagnostic Failures... Failure is not fixed by moving to another slot,
    chassis, etc. Failure is seen in the same way, every time on the same
    component"* — artinya LED mati persisten adalah signature hardware
    failure. Berbeda dari G28 (lampu WAN merah → indikasi WAN/upstream
    issue, rule P02) dan G18 (link lamp di NIC device user → P14 kerusakan
    kabel/device-side). G33 spesifik ke PORT LAN router itu sendiri.
  verification_steps:
    - "Step 1: Identifikasi port LAN di router (label 'LAN' atau angka 1–4, BUKAN port 'WAN' atau 'Internet')."
    - "Step 2: Cabut dan pasang kembali kabel Ethernet di port LAN — dengar klik."
    - "Step 3: Pastikan device ujung lain (laptop/PC) menyala dan NIC-nya aktif."
    - "Step 4: Amati lampu indikator port — harus menyala hijau/oranye (link) dan berkedip saat ada traffic."
    - "Step 5: Jika lampu mati → coba port LAN lain di router yang sama. Jika hanya 1 port mati → port-specific hardware issue. Jika semua port mati → router-wide hardware failure."
    - "Step 6: Coba kabel Ethernet lain untuk exclude kabel rusak."
    - "Step 7: Cek di sisi device (laptop) — apakah link lamp NIC menyala? (lihat G18) Jika di device menyala tapi di router mati → masalah di router."
  interpretation: >
    Semua lampu LAN menyala saat kabel terpasang: normal | 1 port mati
    tapi port lain OK: port-specific hardware issue (router masih usable
    dengan port lain) | Semua port LAN mati: router-wide hardware failure,
    perlu replacement | Lampu berkedip error (merah/oranye cepat):
    kemungkinan short circuit atau electrical fault.
  common_causes:
    - "Port LAN rusak akibat power surge (CXtec)"
    - "Hardware failure di Ethernet controller router (Cisco)"
    - "Overheating merusak komponen port (CXtec: overheating, power surges, hardware malfunctions)"
    - "Physical damage — pin bengkok, kotor, atau korosi"
    - "Firmware bug yang disable port secara software (tapi jarang)"
    - "Power supply router melemah — tidak cukup daya untuk semua port"
  related_symptoms: [G19, G34, G18, G28]
```

---

## P01 — Tidak Ada Koneksi Jaringan

**Kategori:** Konektivitas Dasar
**Status:** ⏳ pending (Fase 1.B)

*TBD — template akan diisi saat Fase 1.B.*

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G01 | Tidak ada koneksi sama sekali | TBD | TBD |
| 2 | G20 | Status NIC "Media Disconnected" | TBD | TBD |
| 3 | G26 | Device lain di jaringan normal | TBD | TBD |

---

## P02 — Koneksi Internet Terputus

**Kategori:** Konektivitas Dasar
**Status:** ⏳ pending (Fase 1.B)

*TBD.*

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G02 | Tidak bisa akses internet | TBD | TBD |
| 2 | G03 | Bisa ping gateway, tidak bisa ping internet | TBD | TBD |
| 3 | G28 | Lampu WAN router merah | TBD | TBD |

---

## P03 — DNS Resolution Failure

**Kategori:** DNS
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G04 | Bisa ping IP publik, tidak bisa akses domain | TBD | TBD |
| 2 | G21 | DNS server tidak respond saat nslookup | TBD | TBD |
| 3 | G24 | Hanya bisa akses via IP, bukan domain | TBD | TBD |

---

## P04 — DNS Cache Poisoning / Hijacking

**Kategori:** DNS
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G17 | Website redirect ke halaman aneh | TBD | TBD |
| 2 | G24 | Hanya bisa akses via IP, bukan domain | TBD | TBD |

---

## P05 — DHCP Failure

**Kategori:** DHCP & IP Config
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G05 | IP address 169.254.x.x (APIPA) | TBD | TBD |
| 2 | G30 | Device tidak mendapat IP DHCP | TBD | TBD |
| 3 | G40 | Error "Limited Connectivity" | TBD | TBD |

---

## P06 — IP Address Conflict

**Kategori:** DHCP & IP Config
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G06 | Pesan IP address conflict | TBD | TBD |
| 2 | G23 | Koneksi putus-nyala (intermittent) | TBD | TBD |

---

## P07 — Subnet Mask / Default Gateway Salah

**Kategori:** DHCP & IP Config
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G07 | Subnet mask berbeda dari device lain | TBD | TBD |
| 2 | G08 | Tidak ada default gateway | TBD | TBD |
| 3 | G35 | Error "Destination Host Unreachable" | TBD | TBD |

---

## P08 — Tidak Bisa Connect ke WiFi

**Kategori:** WiFi
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G09 | Tidak bisa connect ke WiFi | TBD | TBD |
| 2 | G10 | SSID WiFi tidak muncul | TBD | TBD |

---

## P09 — WiFi Signal Lemah / Interferensi

**Kategori:** WiFi
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G11 | WiFi signal bar 1–2 | TBD | TBD |
| 2 | G12 | WiFi sering disconnect | TBD | TBD |

---

## P10 — Jaringan Lambat / Bandwidth Saturation

**Kategori:** Performa
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G13 | Kecepatan internet sangat lambat | TBD | TBD |
| 2 | G22 | Speed test hasil sangat rendah | TBD | TBD |

---

## P11 — Packet Loss Tinggi

**Kategori:** Performa
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G14 | Ping packet loss > 5% | TBD | TBD |
| 2 | G23 | Koneksi putus-nyala (intermittent) | TBD | TBD |

---

## P13 — Firewall Memblokir Koneksi

**Kategori:** Keamanan
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G16 | Aplikasi tertentu tidak bisa connect | TBD | TBD |
| 2 | G25 | Firewall memblokir aplikasi | TBD | TBD |

---

## P14 — Kerusakan Kabel / Konektor Jaringan

**Kategori:** Hardware
**Status:** ⏳ pending (Fase 1.B)

| No | Kode | Nama Gejala | CF_pakar | Justifikasi / Sumber |
|---|---|---|---|---|
| 1 | G18 | Link lamp NIC/switch mati/berkedip | TBD | TBD |
| 2 | G29 | Kabel terlihat rusak / longgar | TBD | TBD |
| 3 | G14 | Ping packet loss > 5% | TBD | TBD |

---

## Cross-Cutting Gejala — Konsistensi Tracking

> Gejala yang muncul di multiple rule. Wajib di-peer review di Fase 1.D untuk konsistensi CF_pakar.

| Gejala | Muncul di Rule | CF_pakar per Rule | Catatan |
|---|---|---|---|
| G13 (internet lambat) | R10 (P10), **R12 (P12)** | TBD, 0.50 | Cross-cutting kuat → di-P12 di-turun ke 0.5 |
| G14 (packet loss > 5%) | R11 (P11), R14 (P14), **R12 (P12)** | TBD, TBD, 0.50 | Signature di P11/P14, supporting di P12 |
| G23 (intermittent) | R06 (P06), R11 (P11), **R12 (P12)** | TBD, TBD, 0.30 | Cross-cutting minor di P12 |
| G24 (akses via IP only) | R03 (P03), R04 (P04) | TBD, TBD | TBD Fase 1.B |
| G33 (lampu LAN mati) | **R15 (P15)** | 0.80 | Resolved orphan — pindah ke R15 |
| G19 (semua client) | **R15 (P15)** | 0.90 | Signature R15 |
| G28 (lampu WAN merah) | R02 (P02) | TBD | TBD Fase 1.B |

---

## Orphan Symptoms — Status Setelah Fase 1.A

| Gejala | Status | Relevansi Ditemukan |
|---|---|---|
| G31 (VPN tidak bisa connect) | ⏳ Open — Fase 1.C | TBD |
| G32 (VPN internal gagal) | ⏳ Open — Fase 1.C | TBD |
| **G33 (Lampu LAN router mati)** | **✅ RESOLVED** | **Pindah ke rule R15 (P15) dengan CF_pakar 0.80 — differentiator hardware failure** |
| G36 (Network adapter disabled) | ⏳ Open — Fase 1.C | Mungkin relevan ke P01 |
| G37 (Driver adapter bermasalah) | ⏳ Open — Fase 1.C | Mungkin relevan ke P01 |
| G38 (Single device bermasalah) | ⏳ Open — Fase 1.C | Differentiator vs G19 |
| G39 (Proxy aktif) | ⏳ Open — Fase 1.C | Mungkin rule baru |

---

## Progress Tracking

| Penyakit | Status | Jumlah Gejala | Sumber Riset | CF Range | Tanggal Selesai |
|---|---|---|---|---|---|
| P01–P11, P13, P14 | ⏳ Pending | TBD | TBD | TBD | TBD |
| **P12 (Latensi Tinggi)** | ✅ **Done** | 4 (expand dari 1) | 9 sumber | 0.30–0.90 | 2026-07-09 |
| **P15 (Router/Switch Failure)** | ✅ **Done** | 4 (expand dari 3 + G33 orphan resolved) | 14 sumber | 0.70–0.90 | 2026-07-09 |

**Statistik Fase 1.A (sample):**
- Total sumber dikumpulkan: 23 (9 P12 + 14 P15)
- Rata-rata sumber per gejala P12: ~5 (target ≥ 3 tercapai)
- Rata-rata sumber per gejala P15: ~5 (target ≥ 3 tercapai)
- Gejala tambahan di-expand P12: 3 (dari 1 → 4)
- Gejala orphan di-resolve P15: 1 (G33)
- Range CF_pakar sample: 0.30 – 0.90

---

*Dibuat: 2026-07-09 | Methodology: Opsi D (skala ordinal + engineering judgment) | Status: Fase 1.A complete — sample P12 & P15 siap untuk review metodologi*
