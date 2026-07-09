
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
**Definisi:** Perangkat sama sekali tidak terhubung ke jaringan — tidak bisa ping gateway, tidak bisa ping lokal, tidak bisa akses internet. Berbeda dari P02 (LAN OK tapi internet putus) — di P01 problemnya adalah di sisi device/NIC/physical layer. Penyebab tersering: NIC disabled, kabel putus, switch port mati, driver rusak.
**Sumber utama riset:**

1. Microsoft Support — "Fix Wi-Fi connection issues in Windows" — https://support.microsoft.com/en-us/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
2. MakeUseOf — "How to Fix 'You Are Not Connected to Any Networks' on Windows" — https://www.makeuseof.com/not-connected-any-networks-error-windows/
3. Tom's Hardware Forum — "Network icon displaying 'Not Connected' and 'No connections are available'" — https://forums.tomshardware.com/threads/network-icon-displaying-not-connected-and-no-connections-are-available.3749720/
4. JustAnswer — "Wi-Fi Disabled on Windows 10? Expert Troubleshooting Guide" — https://www.justanswer.com/computer-networking/uottc-windows-10-wifi-disabled-no-network-icon.html
5. Microsoft Learn Q&A — "Computer won't connect to WiFi, nothing is working to fix it" — https://learn.microsoft.com/en-us/answers/questions/3265166/computer-won-t-connect-to-wifi-nothing-is-working
6. Spiceworks Community — "Icon shows I don't have internet connection but I do?" — https://community.spiceworks.com/t/icon-shows-i-dont-have-internet-connection-but-i-do/273152
7. Microsoft Support — "Fix Ethernet connection problems in Windows" — https://support.microsoft.com/en-us/windows/fix-ethernet-connection-problems-in-windows-2311254e-cab8-42d6-90f3-cb0b9f63645f *(Fase 1.C — G36/G37 device-side diagnosis)*
8. SolveTechToday — "Network Adapter Keeps Turning Itself Off on Windows 11" — https://www.solvetechtoday.com/network-adapter-keeps-disabling-windows-11/ *(Fase 1.C — G36 disabled state differentiation)*
9. WeenDoz — "13 Reasons Why Network Driver Doesn't Work In Windows 10 (and How To Fix It)" — https://weendoz.com/network-driver-windows-10-fix/ *(Fase 1.C — G36 adapter disabled reason #6)*
10. TechSupport4 — "How to Fix Network Adapter Not Working (Windows 10/11)" — https://techsupport4.com/blog/network-adapter-not-working *(Fase 1.C — G36/G37 symptom enumeration)*
11. Intel — "How to Troubleshoot a Yellow Exclamation Mark in Device Manager over the Intel NIC" — https://www.intel.com/content/www/us/en/support/articles/000031131/ethernet-products/gigabit-ethernet-adapters-up-to-2-5gbe.html *(Fase 1.C — G37 driver Code 10)*
12. Microsoft Learn Q&A — "network controller issues (yellow triangle)" — https://learn.microsoft.com/en-us/answers/questions/5635148/network-controller-issues *(Fase 1.C — G37 driver missing)*
13. Windows Central — "How to fix Device Manager yellow mark for drivers on Windows 11" — https://www.windowscentral.com/software-apps/windows-11/how-to-fix-device-manager-yellow-mark-for-drivers-on-windows-11 *(Fase 1.C — G37 yellow mark diagnostic)*
14. ASUS — "Troubleshooting - Yellow exclamation mark in Device Manager" — https://www.asus.com/us/support/faq/1048988/ *(Fase 1.C — G37 vendor troubleshooting)*
15. cr0x.net — "Fix 'No Internet, Secured' by Resetting the Right Network Adapter" — https://cr0x.net/en/reset-right-network-adapter/ *(Fase 1.C — G38 device-isolation decision tree)*

### Tabel CF_pakar

> Rule v1.0.0 berisi G01 + G20 + G26. Identitas P01 = device isolated dari network (single-device scope atau total NIC/physical failure). **Fase 1.C expand:** G36, G37, G38 di-resolve ke R01 sebagai device-side no-connectivity supporting symptoms — memperkuat rule dari 3 → 6 gejala.

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G01** | Tidak ada koneksi sama sekali | **0.85** | 0.9 (signature) | 0.9 → 0.85 (general failure mode) | Definisi problem itu sendiri — zero connectivity. Microsoft Support: classic entry point untuk panduan "fix network issues". MakeUseOf: 'You Are Not Connected to Any Networks' adalah error message spesifik. **Turun** dari 0.9 ke 0.85 karena juga muncul di P02 (internet down → user perception "tidak ada koneksi"), P05 (DHCP failure → no IP → feels like no connectivity), P15 (router down → semua client terdampak tapi bisa dikira P01). Cross-cutting minor di user-perception level. |
| 2 | **G20** | Status NIC "Media Disconnected" | **0.90** | 0.9 (signature) | — | Signature diagnostic indicator — definitif di OS level. Microsoft: `ipconfig` menampilkan "Media: Media disconnected" saat NIC aktif tapi tidak ada link (kabel cabut, switch port mati, atau WiFi disconnected). JustAnswer: panduan Wi-Fi disabled menyertakan check status NIC. Tom's Hardware: thread classic tentang 'Not Connected' indicator. Berbeda dari P15 (semua device affected) — G20 adalah device-specific. |
| 3 | **G26** | Device lain di jaringan normal | **0.80** | 0.7 (common) | 0.7 → 0.8 (differentiator strong) | **Differentiator kuat** antara P01 (device-specific) vs P15 (network-wide). Jika hanya 1 device bermasalah sementara device lain OK → masalah di device tsb (NIC, driver, kabel local). Kontras dengan G19 (semua client affected). **Naik** ke 0.8 karena differentiator menentukan scope troubleshooting (device-side vs network-side). |
| 4 | **G36** | Network adapter disabled | **0.85** | 0.7 (common) | 0.7 → 0.85 (signature device-side, Fase 1.C resolve) | **Resolve dari orphan (Fase 1.C).** Definitif device-side no-connectivity indicator. Microsoft Support (Fix Wi-Fi): *"make sure that the wireless network adapter isn't disabled in Device Manager"* — masuk di daftar step awal troubleshooting. Microsoft Support (Fix Ethernet): Network reset flow eksplisit menyinggung adapter state. SolveTechToday: membedakan "Disabled" (state eksplisit oleh power management atau user) vs "Network cable unplugged" (signal issue) — G36 adalah kategori tersendiri. WeenDoz: "Network adapter disabled in Device Manager" adalah reason #6 dari 13 common causes no-connectivity (quick solution: re-enable di Device Manager). TechSupport4: "common symptoms include ... the adapter showing as disabled". **Naik** dari 0.7 ke 0.85 karena definitif device-side (mirip G20) — berbeda dari G37 yang driver-issue. Min 5 sumber independen. |
| 5 | **G37** | Driver network adapter bermasalah (tanda seru kuning di Device Manager) | **0.80** | 0.7 (common) | 0.7 → 0.80 (signature device-side driver, Fase 1.C resolve) | **Resolve dari orphan (Fase 1.C).** Definitif driver-level indicator. Microsoft Support: *"Outdated, incompatible, or damaged network adapter drivers can prevent network connections or cause intermittent disconnections"* — driver masuk daftar top causes. Microsoft Learn Q&A: *"The yellow triangle means that Windows does not have the correct driver installed for your network hardware"*. Intel KB (yellow exclamation mark NIC): "This device cannot start (Code 10)" — driver problem klasik. Windows Central: yellow mark "almost always is a corruption issue, a missing driver, or a hardware conflict". Driver Talent: *"Unable to connect to the internet: The yellow exclamation mark indicates issues with the network adapter"*. ASUS official troubleshooting halaman sama. **Turun sedikit** dari 0.85 (G36) karena driver issue juga bisa manifest sebagai intermittent (bukan hanya no-connectivity total). Min 6 sumber. |
| 6 | **G38** | Hanya satu perangkat yang bermasalah | **0.80** | 0.7 (common) | 0.7 → 0.80 (inverse G26 differentiator, Fase 1.C resolve) | **Resolve dari orphan (Fase 1.C).** Logically inverse dari G26 ("device lain di jaringan normal"). Dua gejala ini dua sisi coin yang sama — keduanya menandakan **device-specific issue**. Microsoft Support (Fix Ethernet): *"If you have another Windows PC in your home ... try to connect using that PC. If you can connect, the source of the problem is likely due to your first PC"* — explicit device-isolation test. cr0x.net: decision tree untuk isolate adapter/route/DNS selalu dimulai dari swap device test. Karena G26 ditetapkan 0.80, G38 match di 0.80 untuk konsistensi (keduanya adalah differentiator strong dari dua perspektif: G26 = "device lain normal", G38 = "device saya bermasalah"). Min 2 sumber tambahan (sudah covered di G26 sources). |

### Evidence Summary

- **Primary symptom:** G01 (CF 0.85) — user-facing total no connectivity.
- **Diagnostic signature:** G20 (CF 0.9) — ipconfig shows "Media Disconnected" — definitive OS-level.
- **Differentiator pair:** G26 (CF 0.8) + G38 (CF 0.8) — dua sisi coin yang sama, mengisolasi ke device-specific vs network-wide (G19).
- **Device-side failure modes:** G36 (CF 0.85, NIC disabled) + G37 (CF 0.80, driver problem) — strengthen R01 untuk kasus NIC off / driver rusak.
- **Rule P01 (setelah Fase 1.C):** 6 gejala — kombinasi jauh lebih kaya, lolos filter "≥ 2 gejala relevan" di banyak skenario user.
- **Diferensiasi klinis:** G19 (semua affected → P15) vs G26/G38 (device-specific → P01) — G26 & G38 saling memperkuat sebagai differentiator.

### Bundling Tutorial Gejala

#### G01 — Tidak ada koneksi sama sekali

- **short_desc:** Perangkat tidak terhubung ke jaringan sama sekali — icon network menampilkan tanda silang/segita kuning dengan "!". Tidak bisa ping gateway, tidak bisa ping 8.8.8.8, tidak bisa akses website lokal maupun internet.
- **how_to_check:** `Cek icon network di taskbar (silang merah = disconnected, segitiga kuning = limited). Test ping gateway (ipconfig → default gateway → ping <gateway>). Test ping 8.8.8.8. Jika semua gagal → G01.`

```yaml
tutorial:
  definition: >
    "Tidak ada koneksi sama sekali" berarti network-layer connectivity
    total loss — berbeda dari P02 (LAN OK, WAN down) atau P03 (DNS gagal,
    IP still reachable). MakeUseOf: 'You Are Not Connected to Any Networks'
    adalah Windows error spesifik. Microsoft Support klasifikasi root
    cause: adapter disabled, kabel putus, switch port mati, driver corrupt,
    atau Airplane mode aktif. Penting: harus membedakan user-perception
    "tidak ada koneksi" (bisa berarti banyak hal) vs definitif G01 (zero
    connectivity, semua ping gagal).
  verification_steps:
    - "Step 1: Lihat icon network di taskbar. Silang merah = disconnected. Segitiga kuning dengan tanda seru = limited/error."
    - "Step 2: Buka CMD, jalankan `ipconfig /all`. Cek status adapter Anda (Ethernet atau WiFi)."
    - "Step 3: Catat 'Default Gateway' dan 'IPv4 Address'. Jika IPv4 kosong atau 169.254.x.x → lihat P05 (DHCP failure)."
    - "Step 4: Test ping gateway: `ping <gateway-IP> -n 4`. Jika RTO (Request Timed Out) → connectivity ke gateway gagal."
    - "Step 5: Test ping internet IP: `ping 8.8.8.8 -n 4`. Jika gateway OK tapi 8.8.8.8 gagal → lihat P02 (WAN issue)."
    - "Step 6: Jika gateway gagal DAN 8.8.8.8 gagal DAN IPv4 OK → confirmed G01 (P01)."
    - "Step 7: Test ping device lain di jaringan (mis. `ping 192.168.1.X` device lain). Jika gagal juga → device Anda isolated."
    - "Step 8: Cek device lain di jaringan yang sama. Jika mereka normal → G26 (device-specific) → lihat common_causes."
  interpretation: >
    Semua ping gagal + IPv4 OK + device lain normal: confirmed P01
    (device-specific) | Semua ping gagal + IPv4 169.254: P05 (DHCP failure)
    | Gateway OK tapi internet gagal: P02 (WAN issue) | IPv4 OK, gateway
    OK, internet OK tapi DNS gagal: P03 (bukan P01) | Semua device gagal:
    P15 atau P02 (network-wide issue).
  common_causes:
    - "NIC (Network Interface Card) disabled di Windows (Microsoft Support)"
    - "Kabel jaringan putus atau konektor longgar (lihat P14)"
    - "Switch port mati atau router port LAN rusak"
    - "Driver NIC corrupt atau outdated (Tom's Hardware)"
    - "Airplane mode aktif (Windows atau hardware switch)"
    - "NIC hardware failure — kartu fisik rusak"
    - "TCP/IP stack corrupt — perlu netsh int ip reset"
    - "Windows network service stopped — perlu restart service"
  related_symptoms: [G20, G26, G36, G37, G38]
```

#### G20 — Status NIC "Media Disconnected"

- **short_desc:** Output `ipconfig` atau `ipconfig /all` menampilkan "Media State : Media disconnected" pada network adapter — Windows detect adapter tapi tidak ada link layer (physical) connection.
- **how_to_check:** `Buka CMD → jalankan ipconfig /all → cari adapter Anda (Ethernet/WiFi). Lihat field "Media State". Jika "Media disconnected" → G20. Berbeda dari adapter tidak terdeteksi (G36/37).`

```yaml
tutorial:
  definition: >
    "Media Disconnected" adalah status diagnostik OS-level yang
    ditampilkan Windows saat network adapter terdeteksi (driver loaded,
    hardware OK) tapi link-layer (physical connection) tidak establish.
    Berbeda dari P14 (kabel rusak — bisa juga menyebabkan media
    disconnected). Microsoft: kondisi ini menunjukkan NIC enabled tapi
    tidak ada koneksi fisik. JustAnswer: Wi-Fi disabled atau media
    disconnected adalah status classic. Penting: berbeda dari adapter
    tidak terdeteksi di Device Manager (lihat G36/G37).
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Jalankan `ipconfig /all`. Output akan list semua adapter."
    - "Step 3: Cari adapter Anda (biasanya 'Ethernet adapter Ethernet' atau 'Wireless LAN adapter Wi-Fi')."
    - "Step 4: Lihat field `Media State` di bawah adapter tsb. Jika tertulis `Media disconnected` → G20 confirmed."
    - "Step 5: Verifikasi NIC enabled: Device Manager → Network adapters → right-click NIC → Enable (jika currently Disabled)."
    - "Step 6: Untuk Ethernet — cek kabel fisik. Cabut-pasang kabel di kedua ujung (device + switch/router). Dengar klik. Cek lampu link di NIC dan di switch port."
    - "Step 7: Untuk WiFi — cek apakah WiFi toggle ON di taskbar atau Fn-key. Coba connect ke SSID."
    - "Step 8: Untuk konfirmasi hardware vs software — coba di port USB-Ethernet adapter atau WiFi USB. Jika adapter USB OK → masalah hardware NIC original."
    - "Step 9: Restart network service: buka CMD as admin → `net stop dhcp` lalu `net start dhcp`, atau `ipconfig /release` lalu `ipconfig /renew`."
  interpretation: >
    Media disconnected + lampu NIC mati: kabel putus, switch port mati,
    atau NIC hardware issue | Media disconnected + lampu NIC menyala:
    kemungkinan driver issue atau speed/duplex mismatch | WiFi media
    disconnected: WiFi toggle OFF atau adapter disabled | Media disconnected
    setelah disable/enable NIC: normal selama 5-10 detik, kemudian harus
    connect | Media disconnected persisten di semua port: NIC hardware
    rusak.
  common_causes:
    - "Kabel Ethernet putus atau konektor RJ45 longgar (P14)"
    - "Switch port mati atau disabled oleh admin"
    - "WiFi adapter disabled (software atau Fn-key)"
    - "Driver NIC corrupt atau incompatible setelah Windows Update (Tom's Hardware)"
    - "Speed/duplex mismatch antara NIC dan switch (manual 100/full vs auto)"
    - "NIC hardware rusak"
    - "Power management terlalu agresif — Windows disable NIC saat idle"
  related_symptoms: [G01, G26, G36, G37, G18]
```

#### G26 — Device lain di jaringan normal

- **short_desc:** Hanya satu perangkat (atau sebagian kecil) yang bermasalah, sementara device lain di jaringan lokal yang sama bisa konek normal. Indikator bahwa masalah adalah device-specific, bukan network-wide.
- **how_to_check:** `Cek dari minimal 2 device lain di jaringan yang sama (HP, tablet, laptop lain). Jika mereka bisa ping gateway, akses internet, atau buka website → G26 confirmed. Bandingkan dengan G19 (semua affected).`

```yaml
tutorial:
  definition: >
    "Device lain normal" adalah differentiator kuat antara masalah
    device-specific (P01) vs network-wide (P15 atau P02). Kontras dengan
    G19 (semua client terdampak). Penting: harus test device lain DI
    JARINGAN YANG SAMA (bukan hotspot HP atau jaringan tetangga). Untuk
    konfirmasi proper, test device yang terhubung via media yang sama
    (semua Ethernet, atau semua WiFi) — terutama saat debugging P14
    (kabel rusak — hanya device di kabel tsb yang terdampak).
  verification_steps:
    - "Step 1: Identifikasi minimal 2 device lain di lokasi yang sama dan terkoneksi ke jaringan yang sama (HP, tablet, laptop kedua)."
    - "Step 2: Test device lain — buka website (mis. google.com), atau jalankan aplikasi online."
    - "Step 3: Pastikan device lain pakai jaringan yang sama (WiFi SSID yang sama, atau Ethernet di switch yang sama)."
    - "Step 4: Catat hasil: device A normal, device B normal, device C bermasalah → G26 confirmed (device C isolated)."
    - "Step 5: Untuk validasi lebih lanjut — ping gateway dari device normal: `ping <gateway>` harusnya sukses. Bandingkan dengan device bermasalah yang RTO."
    - "Step 6: Untuk kasus P14 (kabel) — test device lain di port yang sama. Pindahkan device normal ke port device bermasalah. Jika device normal juga gagal di port tsb → masalah port/switch (lihat P15)."
    - "Step 7: Untuk kasus WiFi — test device lain di lokasi fisik yang sama. Jika semua device WiFi bermasalah → AP issue (P15 atau P09)."
    - "Step 8: Untuk final confirmation — swap kabel/pantau device. Jika masalah mengikuti device → device-specific. Jika mengikuti port → port-specific."
  interpretation: >
    Hanya 1 device bermasalah, semua device lain normal: confirmed G26 →
    P01 (device-specific) | Beberapa device bermasalah di port/switch
    tertentu: P15 (switch issue) atau P14 (kabel rusak di cluster) |
    Semua device WiFi bermasalah, Ethernet OK: P09 atau P15 (WiFi AP) |
    Semua device (WiFi + Ethernet) bermasalah: G19 (network-wide) → P15
    atau P02.
  common_causes:
    - "Bukan penyebab — G26 adalah differentiator symptom untuk isolasi masalah"
    - "Jika G26 = true → masalah adalah device-specific: NIC, driver, kabel local, atau device-side config"
    - "Jika G26 = false → lihat G19 (network-wide issue → P15 atau P02)"
  related_symptoms: [G01, G19, G20, G38]
```

#### G36 — Network adapter disabled *(Fase 1.C — resolve dari orphan ke R01)*

- **short_desc:** Network adapter (Ethernet atau WiFi) dalam keadaan "Disabled" di Windows — baik di Device Manager (right-click → "Enable device") maupun di Network Connections (`ncpa.cpl`). Bisa terjadi karena user manual disable, Windows power management, atau software third-party (VPN/antivirus). Berbeda dari G20 (NIC enabled tapi no link) dan G37 (NIC ada di Device Manager tapi driver bermasalah).
- **how_to_check:** `Buka Device Manager (Win+X → Device Manager) → expand "Network adapters" → cari adapter Anda. Jika ada icon panah hitam ke bawah (↓) di icon adapter → NIC disabled. Atau buka CMD → jalankan ncpa.cpl → cek apakah adapter tampil abu-abu. Klik kanan → "Enable" untuk re-enable.`

```yaml
tutorial:
  definition: >
    "Network adapter disabled" adalah state eksplisit di mana Windows
    tidak menggunakan NIC tersebut — bukan karena link-layer gagal (G20),
    bukan karena driver rusak (G37), melainkan NIC sengaja dimatikan
    (software state). Microsoft Support (Fix Wi-Fi): "make sure that the
    wireless network adapter isn't disabled in Device Manager" — masuk
    di daftar step awal troubleshooting. SolveTechToday membedakan
    secara tegas: "An adapter that shows as 'Disabled' in Device Manager
    was explicitly disabled — either by Windows power management, or by
    a user or software right-clicking the adapter ... An adapter showing
    as 'Network cable unplugged' or 'Not connected' is still enabled but
    has lost signal." WeenDoz: adapter disabled adalah reason #6 dari 13
    common no-connectivity causes. Penting: cek juga BIOS/UEFI (Onboard
    LAN/Wireless Enable) — jika disabled di firmware, NIC bahkan tidak
    terdeteksi Windows.
  verification_steps:
    - "Step 1: Buka Device Manager (Win+X → Device Manager)."
    - "Step 2: Expand kategori 'Network adapters'."
    - "Step 3: Cari NIC Anda (mis. 'Intel(R) Ethernet Controller', 'Realtek PCIe GbE', 'Intel(R) Wi-Fi 6 AX201')."
    - "Step 4: Amati icon: jika ada panah hitam ke bawah (↓) di icon → NIC disabled (G36)."
    - "Step 5: Alternatif: buka CMD → `ncpa.cpl` → Network Connections window. Jika adapter tampil abu-abu → disabled."
    - "Step 6: Right-click NIC disabled → pilih 'Enable device' (Device Manager) atau 'Enable' (Network Connections). Tunggu 5-10 detik."
    - "Step 7: Setelah enabled, cek di `ipconfig /all` apakah adapter muncul dengan IP. Jika masih 'Media disconnected' → lanjut ke G20."
    - "Step 8: Jika NIC tetap disabled setelah reboot → suspect power management. Buka Device Manager → NIC Properties → tab 'Power Management' → uncheck 'Allow the computer to turn off this device to save power' (SolveTechToday Fix 1)."
    - "Step 9: Jika NIC tidak muncul sama sekali di Device Manager → cek BIOS/UEFI (F2/Del saat boot) → cari 'Onboard LAN' / 'Wireless' → set Enabled (WeenDoz reason #7)."
  interpretation: >
    Icon panah ↓ di NIC: confirmed disabled (G36) → re-enable | NIC
    enabled tapi "Media disconnected": G20 (link issue, lihat P01) | NIC
    ada tapi tanda seru kuning: G37 (driver problem) | NIC tidak muncul
    di Device Manager: disabled di BIOS/UEFI atau hardware failure |
    NIC disable-sendiri berulang: power management agresif atau driver
    crash (SolveTechToday).
  common_causes:
    - "User manual disable (tidak sengaja right-click → Disable)"
    - "Windows power management terlalu agresif — adapter dimatikan saat idle (SolveTechToday)"
    - "Software third-party: VPN client, antivirus, endpoint security yang disable adapter konflik"
    - "Driver crash loop — Windows disable NIC untuk prevent error berulang (SolveTechToday)"
    - "Group Policy atau MDM (Intune) yang disable adapter untuk compliance"
    - "Disabled di BIOS/UEFI (Onboard LAN/Wireless = Off) — NIC bahkan tidak terdeteksi Windows (WeenDoz)"
    - "Hardware switch laptop (Fn-key airplane mode atau switch fisik WiFi)"
  related_symptoms: [G01, G20, G37, G38]
```

#### G37 — Driver network adapter bermasalah *(Fase 1.C — resolve dari orphan ke R01)*

- **short_desc:** Tanda seru kuning (!) di Device Manager pada network adapter — indicator bahwa Windows mendeteksi hardware NIC tapi driver tidak ter-load dengan benar. Klik Properties → tab General menampilkan error code (mis. Code 28 driver not installed, Code 10 cannot start, Code 43 device problem). Bisa juga driver installed tapi incompatible/corrupt setelah Windows Update.
- **how_to_check:** `Buka Device Manager → expand "Network adapters" → cari NIC dengan icon tanda seru kuning. Double-click → tab General → baca "Device status" (mis. "This device cannot start (Code 10)"). Catat error code untuk diagnosis.`

```yaml
tutorial:
  definition: >
    Tanda seru kuning di Device Manager adalah indicator universal bahwa
    sebuah hardware device punya masalah — untuk network adapter,
    hampir selalu driver-level issue. Windows Central: "yellow mark
    almost always is a corruption issue, a missing driver, or a hardware
    conflict." Microsoft Learn Q&A: "The yellow triangle means that
    Windows does not have the correct driver installed for your network
    hardware." Intel KB: tanda seru kuning di NIC biasanya disertai
    error "This device cannot start (Code 10)" — driver load gagal.
    Berbeda dari G36 (NIC disabled — state eksplisit): G37 adalah NIC
    yang aktif di-list tapi tidak function karena driver broken/missing.
    Driver Talent: "Unable to connect to the internet: The yellow
    exclamation mark indicates issues with the network adapter,
    potentially leading to an inability to connect." Microsoft Support:
    "Outdated, incompatible, or damaged network adapter drivers can
    prevent network connections or cause intermittent disconnections."
  verification_steps:
    - "Step 1: Buka Device Manager (Win+X → Device Manager)."
    - "Step 2: Expand 'Network adapters'. Jika ada NIC dengan tanda seru kuning → G37 confirmed."
    - "Step 3: Double-click NIC tsb. Tab 'General' → baca 'Device status'. Catat error code:"
    - "Step 4: Code 28 = driver not installed → perlu install driver dari manufacturer"
    - "Step 5: Code 10 = cannot start → driver load gagal, coba uninstall + restart"
    - "Step 6: Code 31 = driver OK tapi Windows tidak load → update driver"
    - "Step 7: Code 43 = device reported problem → biasanya hardware atau driver critical failure"
    - "Step 8: Code 19 = registry config bad → uninstall device + scan hardware changes"
    - "Step 9: Right-click NIC → 'Update driver' → 'Search automatically' (perlu internet, gunakan USB-Ethernet atau WiFi lain sementara)."
    - "Step 10: Jika update gagal → 'Uninstall device' (centang 'Delete the driver software') → Restart → Windows akan reinstall otomatis. Jika tidak, download driver dari web vendor (Intel/Realtek/Broadcom) via device lain, transfer via USB, install manual."
    - "Step 11: Jika problem muncul setelah Windows Update → tab 'Driver' → 'Roll Back Driver' (Windows Central)."
    - "Step 12: Untuk Intel adapter, pakai Intel Driver & Support Assistant tool (TechSupport4). Untuk lainnya, cari Hardware Ids di tab 'Details' → VEN_xxxx&DEV_xxxx → cari di PCI Lookup."
  interpretation: >
    Code 28 (driver not installed): install driver manufacturer |
    Code 10 (cannot start): uninstall + restart, reinstall driver |
    Code 43 (device problem): suspect hardware failure, coba NIC USB
    lain | Code 37/39 (driver corrupt): uninstall + reinstall | Rollback
    berhasil jika problem mulai setelah Windows Update | NIC USB test
    confirm hardware vs software issue.
  common_causes:
    - "Driver corrupt karena failed Windows Update (Windows Central)"
    - "Driver incompatible setelah upgrade Windows (versi major)"
    - "Driver outdated — tidak support Windows build terbaru"
    - "Driver file corrupt karena disk error atau malware"
    - "Driver salah model — install driver untuk chipset berbeda (WeenDoz reason #3)"
    - "Driver signature enforcement block — driver unsigned (WeenDoz reason #5)"
    - "Conflict dengan security software (antivirus/firewall) yang block driver load"
    - "Conflicting virtual adapter dari VPN client (WeenDoz reason #11)"
  related_symptoms: [G01, G20, G36, G38]
```

#### G38 — Hanya satu perangkat yang bermasalah *(Fase 1.C — resolve dari orphan ke R01)*

- **short_desc:** Hanya satu perangkat (perangkat user) yang mengalami masalah koneksi, sementara semua perangkat lain di jaringan lokal yang sama bisa terhubung normal. Inverse logic dari G26 ("device lain di jaringan normal"). Dua gejala ini dua sisi coin yang sama — keduanya menandakan **device-specific issue** (P01) bukan network-wide (P15/P02).
- **how_to_check:** `Cek minimal 2 device lain di jaringan yang SAMA (WiFi SSID yang sama atau switch Ethernet yang sama). Test: bisa buka website? Bisa ping gateway? Jika device lain normal, hanya device Anda yang bermasalah → G38 confirmed.`

```yaml
tutorial:
  definition: >
    "Hanya satu perangkat bermasalah" adalah mirror/logical-inverse dari
    G26 ("device lain di jaringan normal"). Keduanya menunjukkan scope
    masalah adalah device-specific — bukan network-wide. Microsoft
    Support (Fix Ethernet): "If you have another Windows PC in your
    home and a USB to Ethernet adapter, try to connect using that PC. If
    you can connect, the source of the problem is likely due to your
    first PC." cr0x.net decision tree selalu memulai troubleshooting
    dengan "swap device test" untuk isolate adapter vs network.
    Penting: harus test device lain DI JARINGAN YANG SAMA. Jika device
    lain pakai hotspot HP atau jaringan tetangga → invalid comparison.
    Jika media berbeda (device A WiFi, device B Ethernet) → bisa
    membingungkan (mis. P09 WiFi lemah hanya affect WiFi device, P14
    kabel rusak hanya affect device di kabel tsb).
  verification_steps:
    - "Step 1: Identifikasi minimal 2 device lain di lokasi yang sama (HP, tablet, laptop kedua)."
    - "Step 2: PASTIKAN device lain pakai jaringan yang sama: WiFi SSID yang sama, atau Ethernet di switch yang sama. Jangan compare dengan hotspot HP."
    - "Step 3: Test device lain — buka google.com, atau aplikasi online."
    - "Step 4: Catat hasil: device A normal, device B normal, device C (saya) bermasalah → G38 confirmed."
    - "Step 5: Untuk validasi — ping gateway dari device normal (`ping <gateway>`) → harus sukses. Bandingkan dengan device Anda yang RTO/timeout."
    - "Step 6: Jika hanya device WiFi Anda yang bermasalah, tapi device WiFi lain OK → suspect driver WiFi atau adapter Anda. Test dengan Ethernet jika memungkinkan."
    - "Step 7: Jika hanya device Ethernet Anda yang bermasalah di port tertentu → coba pindahkan ke port lain (lihat P14 kabel atau P15 switch port)."
    - "Step 8: Swap test — pindahkan device Anda ke kabel/port yang dipakai device normal. Jika tetap bermasalah → confirmed device-side. Jika normal → problem di kabel/port asal."
    - "Step 9: Jika semua device bermasalah → bukan G38 melainkan G19 (network-wide) → lihat P15 atau P02."
  interpretation: >
    1 device bermasalah, semua device lain normal: confirmed G38 → P01
    (device-specific) | Beberapa device di port/switch tertentu bermasalah:
    P15 (switch issue) atau P14 (kabel rusak cluster) | Semua device WiFi
    bermasalah, Ethernet OK: P09 (WiFi signal) atau P15 (AP issue) |
    Semua device (WiFi + Ethernet) bermasalah: G19 (network-wide) → P15
    atau P02 | Problem mengikuti device saat swap port: confirmed
    device-side (P01) | Problem mengikuti port: port/switch issue (P15).
  common_causes:
    - "Bukan penyebab — G38 adalah differentiator symptom (mirror G26) untuk isolasi masalah"
    - "Jika G38 = true → masalah adalah device-specific: NIC, driver, kabel local, atau device-side config (lihat G36, G37, G20)"
    - "Jika G38 = false → lihat G19 (network-wide issue → P15 atau P02)"
    - "Perhatikan media: device A via WiFi vs device B via Ethernet bukan comparison valid kecuali P01/P15 umum"
  related_symptoms: [G01, G19, G20, G26, G36, G37]
```

---

