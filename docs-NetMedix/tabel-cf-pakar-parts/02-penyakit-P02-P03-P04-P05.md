## P02 — Koneksi Internet Terputus

**Kategori:** Konektivitas Dasar
**Definisi:** LAN berfungsi normal (bisa ping gateway, device lokal bisa saling communicate), tapi tidak bisa akses internet. Penyebab tersering: WAN putus, ISP outage, NAT misconfig, atau kabel WAN di router tercabut/rusak. Berbeda dari P01 (device isolated) — di P02 semua device terdampak tapi LAN internal masih OK.
**Sumber utama riset:**

1. HighSpeedInternet — "No Internet Connection? How to Troubleshoot Internet Issues" — https://www.highspeedinternet.com/resources/no-internet-connection-troubleshooting-guide
2. BroadbandSearch — "Modem & Router Lights Explained" — https://www.broadbandsearch.net/blog/modem-and-router-lights-meaning-easy-troubleshooting-guide
3. TP-Link — "TP-Link Router Internet Light Off or WAN Port Unplugged: Fix It" — https://www.tp-link.com/us/support/faq/2982/
4. Reddit r/HomeNetworking — "Sudden loss of connectivity to ISP - WAN light solid red on router" — https://www.reddit.com/r/HomeNetworking/comments/14lh1sp/sudden_loss_of_connectivity_to_isp_wan_light/
5. HomeFi — "Router Blinking Red/Orange: Meaning and How to Fix" — https://homefi.info/blogs/homefi-blog/router-blinking-red-orange-meaning-and-how-to-fix
6. Bell Forum — "Modem is flashing red on WAN and no internet service" — https://forum.bell.ca/t5/internet/modem-is-flashing-red-on-wan-and-no-internet-service/td-p/4869
7. cr0x.net — "Fix 'No Internet, Secured' by Resetting the Right Network Adapter" — https://cr0x.net/en/reset-right-network-adapter/ *(Fase 1.C — G39 proxy hijack / leftover config)*
8. ITU Online — "How To Troubleshoot Common VPN Connection Issues" — https://www.ituonline.com/blogs/how-to-troubleshoot-common-vpn-connection-issues-2/ *(Fase 1.C — G39 proxy/VPN overlap)*

### Tabel CF_pakar

> Rule v1.0.0 berisi G02 + G03 + G28. Identitas P02 = WAN-side problem (LAN OK) — berbeda dari P01 (LAN juga down). **Fase 1.C expand:** G39 (proxy aktif) di-resolve ke R02 sebagai cross-cutting minor — proxy misconfig manifest sebagai "no internet" dari user perspective.

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G03** | Bisa ping gateway, tidak bisa ping internet | **0.90** | 0.9 (signature) | — | Signature diagnostic indicator — pattern paling definitive untuk P02 vs P01. Jika gateway reachable tapi 8.8.8.8 RTO → masalah di segment WAN atau upstream router. HighSpeedInternet: panduan triase klasik memakai test ini sebagai pembeda. Reddit r/HomeNetworking: thread classic WAN down scenario. Min 4 sumber. |
| 2 | **G28** | Lampu WAN router merah | **0.85** | 0.7 (common) | 0.7 → 0.85 (differentiator strong) | Differentiator kuat hardware-level — lampu WAN merah berarti modem/router tidak dapat carrier signal dari ISP. BroadbandSearch: *"A red light on a router most commonly means it cannot establish a connection with the modem or that your internet service has been interrupted."* TP-Link: WAN port unplugged issue. HomeFi: blinking red = no WAN IP. **Naik** ke 0.85 karena differentiator strong — lampu WAN spesifik (berbeda dari lampu LAN merah atau lampu WiFi off). |
| 3 | **G02** | Tidak bisa akses internet | **0.50** | 0.7 (common) | 0.7 → 0.5 (general symptom user-facing) | Symptom user-facing yang paling umum tapi juga paling ambiguous — bisa berarti banyak hal (P01 device isolated, P03 DNS, P02 WAN down, P10 throttling, P11 loss parah). HighSpeedInternet: panduan triase. **Turun** dari 0.7 ke 0.5 karena terlalu cross-cutting — tidak boleh mendominasi rule P02. Nilai CF didapat dari triangulasi dengan G03 (definitive) dan G28 (hardware indicator). |
| 4 | **G39** | Proxy setting aktif tanpa sepengetahuan | **0.30** | 0.3 (minor) | 0.3 → 0.30 (cross-cutting minor, Fase 1.C resolve) | **Resolve dari orphan (Fase 1.C).** Proxy misconfig yang user tidak sadari (sisa dari VPN uninstall, malware, atau manual troubleshoot gone wrong) dapat manifest sebagai "no internet" atau "internet aneh/sebagian". cr0x.net: *"If you don't intentionally use a local proxy, reset it to direct (Task 10)"* + *"leftover proxy configuration from VPN/security tooling or manual troubleshooting gone wrong"* + *"If TCP works but Windows still says 'No Internet, secured,' suspect captive portal detection, proxy settings, or NCSI being blocked"*. **Turun ke 0.30** karena: (1) penyebab jarang dibandingkan WAN putus/ISP outage, (2) bukan signature WAN-side problem — lebih ke routing-level misconfig, (3) cross-cutting ke P03 (DNS-like issue bila proxy hijack DNS) dan P13 (firewall-like block). Hanya muncul sebagai supporting evidence di R02, tidak boleh mendominasi. PRD v2.0.0 tidak membuka scope ke rule baru P16 (Proxy Misconfig) — resolve ke R02 adalah jalan tengah terbaik. Min 2 sumber. |

### Evidence Summary

- **Definitive diagnostic:** G03 (CF 0.9) — pattern gateway OK + internet RTO.
- **Hardware indicator:** G28 (CF 0.85) — lampu WAN merah.
- **User-facing general:** G02 (CF 0.5) — turun karena cross-cutting ke banyak problem.
- **Cross-cutting minor:** G39 (CF 0.3) — proxy misconfig sebagai supporting evidence, jarang tapi klinis relevan.
- **Rule P02 (setelah Fase 1.C):** 4 gejala — lolos filter "≥ 2 gejala relevan" dengan kombinasi kaya.
- **Diferensiasi klinis:** G03 (gateway OK, internet RTO) membedakan P02 dari P01 (gateway juga RTO).

### Bundling Tutorial Gejala

#### G02 — Tidak bisa akses internet

- **short_desc:** Browser menampilkan "No internet" / "ERR_INTERNET_DISCONNECTED" / website timeout. Aplikasi online (chat, streaming) tidak bisa connect. Gejala umum yang perlu diagnosis lanjut.
- **how_to_check:** `Coba buka 2-3 website berbeda (mis. google.com, github.com, wikipedia.org). Jika semua timeout atau "No internet" → G02. Lalu jalankan diagnosis lanjut: ping gateway, ping 8.8.8.8, nslookup google.com — untuk menentukan problem layer mana.`

```yaml
tutorial:
  definition: >
    "Tidak bisa akses internet" adalah symptom paling umum dan paling
    ambiguous — bisa disebabkan banyak problem (P01, P02, P03, P10, P11,
    P12). HighSpeedInternet: triase klassik dimulai dengan checklist
    power LED, WAN LED, WiFi LED. Untuk diagnosis proper, G02 harus
    dikombinasikan dengan G03 (gateway ping test) untuk membedakan scope
    problem. Bisa juga disebabkan aplikasi-side issue (mis. browser cache,
    proxy aktif — G39).
  verification_steps:
    - "Step 1: Buka browser, coba akses 2-3 website berbeda (mis. google.com, github.com, wikipedia.org)."
    - "Step 2: Jika semua timeout/error → G02. Catat error message (mis. ERR_INTERNET_DISCONNECTED, ERR_NAME_NOT_RESOLVED, ERR_CONNECTION_REFUSED)."
    - "Step 3: Buka CMD, jalankan `ipconfig`. Catat 'Default Gateway' (mis. 192.168.1.1)."
    - "Step 4: Test ping gateway: `ping 192.168.1.1 -n 4`. Jika RTO → G03 negatif (tidak bisa ping gateway) → lihat P01."
    - "Step 5: Jika gateway OK → test ping internet IP: `ping 8.8.8.8 -n 4`. Jika RTO → G03 confirmed → P02."
    - "Step 6: Jika gateway OK dan 8.8.8.8 OK tapi website gagal → DNS issue → lihat G04/G21 (P03)."
    - "Step 7: Test aplikasi online lain (chat, email). Jika hanya browser yang gagal → browser-specific issue (cache, proxy)."
    - "Step 8: Cek juga apakah device lain di jaringan juga tidak bisa internet (G19) — jika semua terdampak → network-wide issue (P02 atau P15)."
  interpretation: >
    Semua ping gagal: P01 | Gateway OK, internet RTO: G03 → P02 | Gateway
    OK, internet OK, DNS gagal: P03 | Hanya browser gagal: browser cache
    atau proxy (G39) | Hanya aplikasi tertentu gagal: G16 (P13) | Semua
    device terdampak + lampu WAN merah: confirmed P02 (G28).
  common_causes:
    - "WAN koneksi ke ISP putus (G03, G28)"
    - "ISP outage (cek status ISP atau hubungi support)"
    - "NAT atau routing misconfig di router (P15-related)"
    - "DNS server gagal (separate dari WAN — P03)"
    - "Proxy aktif tanpa sepengetahuan (G39)"
    - "Browser cache corrupt atau malware"
    - "Firewall terlalu ketat (P13)"
  related_symptoms: [G03, G28, G19, G04, G39]
```

#### G03 — Bisa ping gateway, tidak bisa ping internet

- **short_desc:** Saat test ping, gateway (mis. 192.168.1.1) respond normal, tapi ping ke internet IP (mis. 8.8.8.8, 1.1.1.1) gagal/RTO. Pattern definitif WAN-side problem.
- **how_to_check:** `Buka CMD. Jalankan: ipconfig → catat default gateway. Lalu: ping <gateway> -n 4 (harus sukses). Lanjut: ping 8.8.8.8 -n 4 (jika RTO → G03 confirmed).`

```yaml
tutorial:
  definition: >
    Pattern "gateway OK + internet RTO" adalah signature definitif masalah
    di segment WAN atau upstream router. Berbeda dari P01 (gateway juga
    RTO — LAN down). Mekanisme: LAN-side routing ke gateway via switch/AP
    OK, tapi router tidak bisa forward traffic ke internet (WAN putus,
    NAT gagal, atau upstream ISP down). HighSpeedInternet: panduan triase
    utama memakai test ini sebagai pembeda scope. Reddit r/HomeNetworking:
    classic WAN down scenario dengan pattern ini.
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Jalankan `ipconfig`. Catat 'Default Gateway' (mis. 192.168.1.1)."
    - "Step 3: Test ping gateway: `ping 192.168.1.1 -n 4`. Jika sukses (Reply from 192.168.1.1: bytes=32 time=Xms) → gateway OK."
    - "Step 4: Jika gateway RTO → BUKAN P02. Lihat P01 atau P15."
    - "Step 5: Test ping internet IP: `ping 8.8.8.8 -n 4`. Jika RTO → G03 confirmed."
    - "Step 6: Untuk isolasi DNS vs WAN — coba ping 1.1.1.1 juga. Jika keduanya RTO → WAN issue confirmed."
    - "Step 7: Untuk konfirmasi WAN-side vs NAT issue — login ke router admin (http://192.168.1.1), cek status WAN. Router biasanya menampilkan 'WAN Status: Disconnected' atau 'WAN IP: 0.0.0.0' jika WAN down."
    - "Step 8: Cek juga lampu WAN di router (lihat G28). Jika merah atau off → confirmed WAN issue."
    - "Step 9: Test dari device lain di jaringan yang sama. Jika pattern G03 konsisten di semua device → network-wide WAN issue (P02 atau P15)."
  interpretation: >
    Gateway OK + 8.8.8.8 RTO + 1.1.1.1 RTO: definitif WAN issue (P02) |
    Gateway OK + 8.8.8.8 RTO tapi 1.1.1.1 OK: aneh, mungkin specific route
    block | Gateway OK + semua IP internet RTO + nslookup RTO: WAN atau
    DNS-double-failure | Gateway OK + ping internet OK tapi domain gagal:
    P03 (DNS), bukan P02 | Router admin tidak accessible + G03: P15 (router
    hang).
  common_causes:
    - "WAN link ke ISP putus (fisik atau logical)"
    - "ISP outage (check downdetector.com atau ISP status page)"
    - "Router NAT misconfig atau NAT table full"
    - "WAN port kabel rusak atau tercabut (TP-Link)"
    - "ISP throttling atau blocked karena billing issue"
    - "WAN IP lease dari ISP expired, router belum renegotiate"
    - "PPPoE credential salah (untuk DSL/fiber)"
  related_symptoms: [G02, G28, G19]
```

#### G28 — Lampu WAN router merah

- **short_desc:** Indikator LED berlabel "WAN" atau "Internet" di router/modem menyala merah, berkedip merah, atau off sama sekali (padahal router ON). Definitif hardware-level WAN problem.
- **how_to_check:** `Lihat fisik router/modem. Identifikasi LED berlabel "WAN", "Internet", atau globe icon. Warna normal: hijau/biru. Warna problem: merah, orange, atau off. Jika merah/berkedip merah → G28.`

```yaml
tutorial:
  definition: >
    Lampu WAN/Internet di router adalah indicator link-layer connection
    antara router dan ISP (via modem ONT atau direct Ethernet ke ISP).
    BroadbandSearch: "A red light on a router most commonly means it
    cannot establish a connection with the modem or that your internet
    service has been interrupted." TP-Link: WAN port unplugged issue.
    HomeFi: blinking red = no WAN IP atau ISP issue. Berbeda dari G33
    (lampu LAN mati → P15 hardware LAN port) — G28 spesifik untuk WAN
    side.
  verification_steps:
    - "Step 1: Identifikasi router/modem fisik. Cari LED berlabel 'WAN', 'Internet', atau globe icon (@)."
    - "Step 2: Amati warna LED: hijau/biru solid = normal | merah solid = WAN problem | merah berkedip = WAN trying to connect | off = WAN port unplugged atau router off."
    - "Step 3: Jika merah/berkedip → cek kabel WAN di router. Kabel WAN biasanya label 'WAN' atau 'Internet' (bukan 'LAN' 1-4)."
    - "Step 4: Cabut dan pasang kembali kabel WAN di router DAN di modem (jika modem separate). Dengar klik di kedua ujung."
    - "Step 5: Coba kabel Ethernet lain (yang sudah di-test working) untuk exclude kabel rusak."
    - "Step 6: Restart modem dan router. Cabut power keduanya, tunggu 60 detik, pasang modem dulu (tunggu 2 menit stabilize), lalu router (tunggu 2 menit)."
    - "Step 7: Setelah restart, amati LED WAN. Jika hijau dalam 5 menit → problem solved (transient). Jika masih merah → ISP outage atau hardware issue."
    - "Step 8: Untuk konfirmasi ISP outage — cek status page ISP (mis. telkom.co.id, indihome.co.id) atau downdetector.com. Hubungi ISP support jika perlu."
    - "Step 9: Untuk modem fiber/ONT — cek juga lampu PON/LOS di ONT. LOS (Loss of Signal) merah = fiber putus atau dirty connector."
  interpretation: >
    LED WAN hijau solid: normal, WAN link OK | LED WAN hijau berkedip:
    sedang transfer data, normal | LED WAN merah solid: WAN link gagal
    establish | LED WAN merah berkedip: trying to connect (ISP issue atau
    authentication) | LED WAN off: kabel WAN unplugged atau router WAN
    port rusak | LED LOS merah di ONT: fiber putus, kontak ISP.
  common_causes:
    - "WAN kabel putus atau tercabut (TP-Link)"
    - "ISP outage atau maintenance (BroadbandSearch)"
    - "Modem/ONT rusak atau reboot loop"
    - "PPPoE atau DHCP-from-ISP credential salah"
    - "MAC address binding ISP yang tidak match dengan router baru"
    - "ISP throttling/blocked karena billing issue"
    - "WAN port di router rusak (hardware failure)"
    - "Fiber cut atau dirty connector (untuk fiber connection)"
  related_symptoms: [G02, G03, G19]
```

#### G39 — Proxy setting aktif tanpa sepengetahuan *(Fase 1.C — resolve dari orphan ke R02)*

- **short_desc:** Browser atau Windows memiliki setting proxy yang aktif (mis. proxy 127.0.0.1:8080 atau corporate proxy) tanpa user mengetahui asalnya. Biasanya sisa dari: (a) VPN client yang di-uninstall tapi tidak clean up proxy entry, (b) malware/PUP yang set proxy untuk intercept traffic, (c) corporate IT policy yang persist setelah device keluar dari managed environment, atau (d) manual troubleshoot yang lupa di-reset. Symptom: internet bisa "sebagian" (browser gagal tapi app lain OK), atau "No Internet, Secured" padahal TCP ke IP luar masih work.
- **how_to_check:** `Windows: Settings → Network & Internet → Proxy. Cek "Use a proxy server" — harusnya OFF untuk home user. Atau CMD: netsh winhttp show proxy (harus "Direct access (no proxy server)"). Browser Chrome/Edge: Settings → System → Open your computer's proxy settings. Firefox: Settings → Network Settings → "Use system proxy" atau "No proxy".`

```yaml
tutorial:
  definition: >
    Proxy setting yang aktif tanpa user sadari adalah sumber umum "no
    internet" atau "internet aneh" yang sering terlewat. cr0x.net:
    "If you don't intentionally use a local proxy, reset it to direct"
    — dan menempatkan proxy reset di decision tree "No Internet, Secured"
    bersama captive portal dan NCSI block. cr0x.net: "leftover proxy
    configuration from VPN/security tooling or manual troubleshooting
    gone wrong" — proxy orphan adalah pattern klasik post-uninstall.
    ITU Online: VPN clients yang gagal clean up bisa meninggalkan proxy
    adapter virtual yang intercept traffic. Berbeda dari P03 (DNS gagal
    total) — di G39 DNS masih bisa resolve via proxy jika proxy hidup,
    tapi browser gagal karena proxy target sudah mati. Juga berbeda dari
    P02 (WAN putus) — di G39 WAN link OK tapi traffic di-hijack ke
    proxy mati. Manifest: "sebagian app jalan, sebagian gagal", "browser
    gagal tapi ping 8.8.8.8 OK", atau "ERR_PROXY_CONNECTION_FAILED".
  verification_steps:
    - "Step 1: Buka Windows Settings → Network & Internet → Proxy."
    - "Step 2: Cek section 'Manual proxy setup' → 'Use a proxy server'. Jika ON dan Anda tidak tahu kenapa → suspect G39."
    - "Step 3: Untuk konfirmasi command-line, buka CMD as admin → `netsh winhttp show proxy`. Output normal: 'Direct access (no proxy server)'. Jika menampilkan proxy server → confirmed."
    - "Step 4: Cek juga browser-specific proxy: Firefox bisa override system proxy (Settings → Network Settings). Chrome/Edge pakai system proxy."
    - "Step 5: Cek registry proxy setting: `reg query \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\" /v ProxyEnable`. Jika ProxyEnable=1 → proxy aktif."
    - "Step 6: Test dengan proxy OFF sementara — Settings → Proxy → toggle OFF → coba buka website. Jika internet kembali → confirmed G39."
    - "Step 7: Reset WinHTTP proxy ke direct: CMD as admin → `netsh winhttp reset proxy`. Output: 'Direct access (no proxy server)'."
    - "Step 8: Cek juga apakah ada PAC file (Web Proxy Auto-Discovery) — Settings → Proxy → 'Use setup script'. Jika ON dan Anda tidak tahu → disable."
    - "Step 9: Scan malware/PUP (ProxyTrojan, PUP.Optional.Proxy) menggunakan Malwarebytes atau Windows Defender Offline — proxy orphan kadang adalah malware C2."
    - "Step 10: Cek VPN client terinstall: uninstall melalui Settings → Apps, lalu cek proxy reset. Beberapa VPN (NordVPN, ExpressVPN, corporate VPN) set proxy saat connect tapi gagal reset saat uninstall."
  interpretation: >
    Proxy ON tanpa sepengetahuan + internet sebagian gagal: confirmed G39
    | Proxy ON + ERR_PROXY_CONNECTION_FAILED di browser: proxy target
    mati | Proxy OFF tapi internet kembali: confirmed leftover proxy
    (G39) | netsh winhttp show proxy = 'Direct access': tidak ada system
    proxy, tapi cek juga Firefox/browser-specific | ProxyEnable=1 di
    registry tapi Proxy OFF di Settings: malware atau GPO override |
    Proxy PAC file aktif: WPAD hijack atau corporate policy.
  common_causes:
    - "Sisa VPN client yang gagal clean up proxy entry (cr0x.net, ITU Online)"
    - "Malware/PUP yang set proxy untuk intercept atau inject ads"
    - "Corporate IT policy (GPO/Intune) yang persist setelah device leave managed environment"
    - "Manual troubleshoot yang lupa di-reset (mis. set proxy untuk Fiddler/Burp debugging)"
    - "WPAD (Web Proxy Auto-Discovery) hijack via rogue DHCP/DNS"
    - "Browser extension yang set proxy tanpa consent"
    - "Captive portal yang set proxy saat connect ke public WiFi tapi tidak clear saat disconnect"
  related_symptoms: [G02, G03, G16, G25]
```

---

## P03 — DNS Resolution Failure

**Kategori:** DNS
**Definisi:** IP-layer connectivity OK (bisa ping 8.8.8.8), tapi name resolution gagal — domain tidak bisa di-resolve ke IP. Penyebab tersering: DNS server tidak respond, DNS setting kosong di adapter, atau DNS cache corrupt. Berbeda dari P04 (cache poisoning — DNS respond tapi salah), di P03 DNS server tidak respond atau resolver tidak terjangkau.
**Sumber utama riset:**

1. Microsoft Learn — "Troubleshooting DNS Servers" — https://learn.microsoft.com/en-us/windows-server/networking/dns/troubleshoot/troubleshoot-dns-server
2. OneUptime — "How to Troubleshoot DNS Resolution Issues with dig and nslookup" — https://oneuptime.com/blog/post/2026-03-04-troubleshoot-dns-resolution-issues-with-dig-and-nslookup/view
3. UptimeRobot — "DNS Server Not Responding: Causes, Fixes, and Prevention Guide" — https://uptimerobot.com/knowledge-hub/monitoring/how-to-fix-dns-server-not-responding-error/
4. NsLookup.io — "How to Fix 'DNS Server Not Responding': Step-by-Step" — https://www.nslookup.io/learning/dns-server-not-responding/
5. Spiceworks Community — "NSLOOKUP not finding DNS server" — https://community.spiceworks.com/t/nslookup-not-finding-dns-server/466226
6. TechRepublic — "DNS Problems nslookup failing" — https://www.techrepublic.com/forums/discussions/dns-problems-nslookup-failing/

### Tabel CF_pakar

> Rule v1.0.0 berisi G04 + G21 + G24. Identitas P03 = DNS server tidak respond atau DNS layer total gagal — berbeda dari P04 (server respond tapi salah).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G21** | DNS server tidak respond saat nslookup | **0.95** | 0.9 (signature) | 0.9 → 0.95 (definitive diagnostic tool) | Definisi problem itu sendiri — `nslookup` dan `dig` adalah standard industri untuk verifikasi DNS. Microsoft Learn: *"If the resolver returns a 'Request to server timed out' or 'No response from server' response, the DNS service probably is not running."* NsLookup.io & UptimeRobot — panduan komprehensif memakai nslookup sebagai primary diagnostic. OneUptime: panduan dig untuk P03. **Naik** ke 0.95 karena definitive — output nslookup "server timed out" hampir tidak ada false positive. |
| 2 | **G04** | Bisa ping IP publik, tidak bisa akses domain | **0.85** | 0.7 (common) | 0.7 → 0.85 (differentiator strong) | Pattern definitif isolasi DNS vs IP-layer. Microsoft Learn: klasik triase DNS. OneUptime & UptimeRobot: panduan utama memakai test ini sebagai pembeda P03 dari P02 (WAN down). **Naik** ke 0.85 karena differentiator kuat — IP ping works tapi domain fails = DNS layer problem (P03 atau P04). |
| 3 | **G24** | Hanya bisa akses via IP, bukan domain | **0.90** | 0.9 (signature) | — | Di P03, G24 adalah **signature kuat (0.9)** — berbeda dari P04 (0.5, supporting). Justifikasi: di P03 DNS TOTAL gagal resolve → user observe symptom G24 dengan clarity tinggi. Di P04, DNS masih resolve tapi ke IP salah → G24 kurang definitive. Konsistensi: G24 dengan CF 0.9 di P03 adalah signature, dengan CF 0.5 di P04 supporting — sesuai metodologi Opsi D (nilai CF boleh berbeda per konteks rule). Lihat bundling G24 di P04. |

### Evidence Summary

- **Diagnostic signature:** G21 (CF 0.95) — nslookup definitive timeout.
- **Pattern differentiator:** G04 (CF 0.85) — IP works, domain fails.
- **User-facing signature:** G24 (CF 0.9) — akses via IP only.
- **Rule P03:** 3 gejala — lolos filter "≥ 2 gejala relevan" dengan kombinasi kaya.
- **Diferensiasi klinis:** G21 (timeout) membedakan P03 dari P04 (nslookup return IP salah).

### Bundling Tutorial Gejala

#### G04 — Bisa ping IP publik, tidak bisa akses domain

- **short_desc:** Test ping ke IP publik (8.8.8.8, 1.1.1.1) sukses, tapi test ping ke domain (google.com, cloudflare.com) gagal dengan "Could not find host" / "DNS Resolution failed".
- **how_to_check:** `Ping 8.8.8.8 -n 4 (harus sukses). Lalu ping google.com -n 4 (jika gagal dengan "could not find host" → G04 confirmed).`

```yaml
tutorial:
  definition: >
    Pattern "IP ping works, domain ping fails" adalah signature definitif
    DNS-layer problem (P03 atau P04). Microsoft Learn: panduan triase DNS
    klassik memakai pattern ini. Mekanisme: IP-layer routing OK (bisa
    reach 8.8.8.8 via routing table), tapi name resolution gagal — domain
    tidak bisa di-translate ke IP. OneUptime: dig command guide untuk
    isolasi DNS issue. Berbeda dari P02 (WAN down — IP publik juga RTO).
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Test ping IP publik: `ping 8.8.8.8 -n 4`. Jika RTO → lihat P02 (WAN issue), BUKAN P03."
    - "Step 3: Jika 8.8.8.8 OK → test ping domain: `ping google.com -n 4`. Jika gagal dengan 'Ping request could not find host google.com' → G04 confirmed."
    - "Step 4: Test juga `ping 1.1.1.1` dan `ping cloudflare.com` untuk konfirmasi konsistensi pattern."
    - "Step 5: Untuk isolasi DNS lokal vs upstream — jalankan `nslookup google.com` (lihat G21 untuk detail)."
    - "Step 6: Test dengan DNS publik: `nslookup google.com 8.8.8.8`. Jika respond → DNS lokal adapter yang bermasalah. Jika juga timeout → DNS upstream issue."
    - "Step 7: Coba akses website via IP langsung: ketik `https://142.250.193.78` di browser. Jika OK → confirmed DNS issue (lihat G24)."
    - "Step 8: Test flush DNS cache: `ipconfig /flushdns` lalu retry. Jika resolved → cache corrupt."
  interpretation: >
    IP works + domain fails: definitif DNS issue (P03 atau P04) | IP
    works + domain works: normal | IP fails + domain fails: P02 (WAN) |
    IP works + nslookup timeout: P03 (DNS failure) | IP works + nslookup
    return IP salah: P04 (DNS poisoning) | Flush DNS solves: cache
    corrupt (transient).
  common_causes:
    - "DNS server tidak respond (P03)"
    - "DNS setting adapter kosong atau IP invalid (Microsoft Learn)"
    - "DNS cache corrupt (sebagian P03, sebagian P04)"
    - "DNS server upstream down atau unreachable"
    - "Firewall blocks DNS port (UDP/TCP 53)"
    - "DNS service Windows stopped — perlu restart service"
  related_symptoms: [G21, G24, G17, G02]
```

#### G21 — DNS server tidak respond saat nslookup

- **short_desc:** Output `nslookup <domain>` menampilkan "Default Server: UnKnown" + "DNS request timed out" atau "Can't find server name for address X: No response from server". Definitif DNS server unreachable atau service down.
- **how_to_check:** `Buka CMD → jalankan nslookup google.com → tunggu 5-15 detik. Jika "DNS request timed out, timeout was 2 seconds" atau "No response from server" → G21. Bandingkan dengan nslookup google.com 8.8.8.8 (DNS Google).`

```yaml
tutorial:
  definition: >
    `nslookup` adalah tool bawaan Windows/Linux untuk query DNS server
    langsung. Microsoft Learn: "If the resolver returns a 'Request to
    server timed out' or 'No response from server' response, the DNS
    service probably is not running." NsLookup.io & UptimeRobot: panduan
    definitif memakai nslookup sebagai diagnostic DNS utama. Output
    "Default Server: UnKnown" berarti adapter DNS setting tidak ter-config
    dengan benar. Output "DNS request timed out" berarti DNS server
    unreachable.
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Jalankan `nslookup google.com`. Output default akan menampilkan: 'Default Server: <server-name>' dan 'Address: <DNS-IP>'."
    - "Step 3: Catat 'Default Server' dan 'Address'. Jika server name 'UnKnown' atau address kosong/0.0.0.0 → adapter DNS setting bermasalah."
    - "Step 4: Tunggu hasil query. Jika 'DNS request timed out, timeout was 2 seconds' berulang → G21 confirmed."
    - "Step 5: Test dengan DNS publik: `nslookup google.com 8.8.8.8`. Jika respond cepat → DNS lokal adapter yang bermasalah (perlu update setting)."
    - "Step 6: Jika nslookup ke 8.8.8.8 juga timeout → DNS port (53) mungkin di-block firewall atau ISP (jarang)."
    - "Step 7: Cek DNS setting adapter: `ipconfig /all` → cari 'DNS Servers' di adapter Anda. Catat IP DNS."
    - "Step 8: Test ping IP DNS server: `ping <DNS-IP>`. Jika RTO → DNS server unreachable. Jika OK tapi nslookup timeout → DNS service problem."
    - "Step 9: Untuk fix DNS lokal: ganti DNS ke 8.8.8.8 atau 1.1.1.1 (Settings → Network → adapter Properties → IPv4 → Use following DNS server addresses)."
  interpretation: >
    nslookup respond cepat + IP benar: normal, DNS OK | nslookup timeout
    + DNS lokal tapi via 8.8.8.8 OK: DNS lokal bermasalah, ganti ke 8.8.8.8
    | nslookup timeout di semua DNS server: firewall block port 53 atau
    ISP filter | 'Default Server: UnKnown': adapter DNS setting kosong
    | nslookup return IP salah: P04 (poisoning), bukan P03.
  common_causes:
    - "DNS server tidak respond (Microsoft Learn)"
    - "DNS service di Windows stopped atau crash"
    - "DNS setting adapter kosong atau 0.0.0.0"
    - "DNS server upstream (ISP) down"
    - "Firewall blok UDP/TCP port 53"
    - "DNS cache lokal Windows corrupt (perlu flush)"
    - "Router DNS forwarder salah konfigurasi"
  related_symptoms: [G04, G24, G17, G02]
```

#### G24 — Hanya bisa akses via IP, bukan domain

> **Cross-reference:** Lihat bundling lengkap di P04 (DNS Cache Poisoning). Di P03, G24 adalah **signature kuat (CF 0.9)** karena DNS total gagal resolve — user observe G24 dengan clarity tinggi. Berbeda dari P04 (CF 0.5 — supporting karena DNS masih resolve ke IP salah). Konsistensi cross-cutting: nilai CF berbeda per konteks rule sesuai metodologi Opsi D.

---

## P04 — DNS Cache Poisoning / Hijacking

**Kategori:** DNS
**Definisi:** Domain di-resolve ke IP yang salah akibat cache DNS lokal/solver dikompromi (poisoning) atau response DNS dimanipulasi (hijacking). Berbeda dari P03 (DNS resolution failure — server tidak respond), di P04 server respond tapi jawabannya SALAH. User diarahkan ke situs palsu/malicious.
**Sumber utama riset:**

1. Palo Alto Networks — "What Is DNS Hijacking?" — https://www.paloaltonetworks.com/cyberpedia/what-is-dns-hijacking
2. Huntress — "What Is DNS Poisoning? Attacks & Prevention Guide" — https://www.huntress.com/cybersecurity-101/topic/what-is-dns-poisoning-cybersecurity-guide
3. Infoblox — "What are DNS spoofing, DNS hijacking and DNS cache poisoning?" — https://www.infoblox.com/dns-security-resource-center/what-are-dns-spoofing-dns-hijacking-dns-cache-poisoning/
4. Kaspersky — "What is DNS hijacking? Detection & Prevention" — https://www.kaspersky.com/resource-center/definitions/what-is-dns-hijacking
5. CSC (CSC Digital Brand Services) — "DNS Poisoning: Prevention and Protection Strategies" — https://www.cscdbs.com/en/resources/dns-poisoning/
6. Heimdalsecurity — "Domain Hijacking vs DNS Poisoning: Do You Know the Difference?" — https://heimdalsecurity.com/blog/domain-hijacking-vs-dns-poisoning-do-you-know-the-difference/
7. Office1 — "DNS Hijacking: What it is and How to Protect Your Business" — https://www.office1.com/blog/what-is-a-dns-hijacking

### Tabel CF_pakar

> Rule v1.0.0 berisi G17 + G24. Identitas P04 = malicious redirect (G17) yang membedakan dari P03 (DNS putus total).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G17** | Website redirect ke halaman aneh | **0.90** | 0.7 (common) | 0.7 → 0.9 (signature differentiator) | **Signature symptom** P04 — membedakan dari P03 (DNS gagal total). Huntress: *"Detecting DNS poisoning can include warning signs such as unexpected website redirects, SSL certificate warnings, anomalies in DNS logs."* Palo Alto: *"DNS hijacking is a type of attack where attackers manipulate DNS responses to redirect users to unauthorized or malicious destinations."* Kaspersky, CSC, Heimdalsecurity — semua konsisten menyebut unexpected redirect sebagai primary indicator. **Naik** ke 0.9 karena differentiator unik antara P04 (redirect ke malicious) vs P03 (tidak resolve sama sekali). Min 5 sumber. |
| 2 | **G24** | Hanya bisa akses via IP, bukan domain | **0.50** | 0.7 (common) | 0.7 → 0.5 (cross-cutting dengan P03) | Common symptom tapi cross-cutting dengan P03 (di mana G24 adalah signature 0.9). Infoblox: *"Cache poisoning is a more specific type of attack targeting caching name servers in an attempt to control the answers stored in the DNS cache."* Saat cache corrupt, domain bisa resolve ke IP salah — user bisa saja masih akses via IP langsung (mis. `https://142.250.x.x`) tapi domain gagal atau salah. **Turun** karena di P03 G24 adalah signature (0.9); di P04 G24 cuma supporting karena yang lebih spesifik adalah redirect (G17). Konsistensi cross-cutting tracking. |

### Evidence Summary

- **Signature symptom:** G17 (CF 0.9) — redirect ke halaman aneh adalah differentiator unik P04.
- **Supporting symptom:** G24 (CF 0.5) — cross-cutting dengan P03, di P04 hanya supporting.
- **Rule P04:** 2 gejala — lolos filter "≥ 2 gejala relevan".
- **Diferensiasi klinis:** G17 (redirect) membedakan P04 (cache berisi jawaban SALAH) dari P03 (cache TIDAK ADA jawaban / server timeout).

### Bundling Tutorial Gejala

#### G17 — Website redirect ke halaman aneh

- **short_desc:** Saat mengetik URL website yang dikenal (mis. google.com, bank Anda), browser diarahkan ke halaman berbeda — bisa halaman blank, situs typo-squatting mirip asli, atau IP raw.
- **how_to_check:** `Coba akses website dikenal via domain (mis. https://google.com). Lalu akses via IP langsung (mis. https://142.250.193.78). Jika via domain redirect aneh tapi via IP OK → curiga DNS poisoning. Konfirmasi dengan nslookup domain → bandingkan IP hasil dengan IP resmi (via DNS lain seperti 8.8.8.8).`

```yaml
tutorial:
  definition: >
    DNS cache poisoning/hijacking adalah kondisi di mana DNS resolver cache
    berisi mapping domain→IP yang SALAH — biasanya akibat serangan
    (malware, rogue DHCP, MITM) atau misconfiguration. Berbeda dari P03
    (DNS resolution failure — server tidak respond), di P04 server merespon
    tapi dengan jawaban malicious. Huntress: "Detecting DNS poisoning can
    include warning signs such as unexpected website redirects, SSL
    certificate warnings, anomalies in DNS logs, and exfiltrated data."
    Palo Alto: "Attackers manipulate DNS responses to redirect users to
    unauthorized or malicious destinations." Tanda spesifik: SSL warning
    mendadak di site yang biasanya OK (karena cert IP palsu tidak match
    domain asli).
  verification_steps:
    - "Step 1: Pilih 3-5 website dikenal yang biasanya Anda akses tanpa masalah (mis. google.com, github.com, bank Anda)."
    - "Step 2: Akses masing-masing via browser. Amati apakah ada yang redirect ke halaman aneh, blank, atau warning SSL/certificate error."
    - "Step 3: Jika ada redirect — catat URL tujuan. Bandingkan dengan URL yang diharapkan."
    - "Step 4: Jalankan `nslookup <domain>` di CMD/Terminal. Catat IP yang di-return."
    - "Step 5: Bandingkan dengan query via DNS publik: `nslookup <domain> 8.8.8.8` (pakai DNS Google). Jika IP hasil berbeda → indikasi kuat poisoning di DNS lokal."
    - "Step 6: Test akses via IP langsung: ketik `https://<IP-asli>` di browser. Jika via IP berhasil muncul situs asli tapi via domain redirect → confirmed DNS issue (P03 atau P04)."
    - "Step 7: Untuk konfirmasi P04 (poisoning) vs P03 (failure) — cek apakah DNS server respond: `nslookup` tanpa argumen harusnya menampilkan server name. Jika respond tapi jawaban salah → P04. Jika timeout → P03."
  interpretation: >
    Semua site akses normal: tidak ada poisoning | 1-2 site redirect tapi
    via IP OK: mungkin CDN/regional routing anomaly | Banyak site redirect
    aneh + SSL warning mendadak: indikasi kuat DNS poisoning | Hasil
    nslookup berbeda antara DNS lokal vs 8.8.8.8: confirmed cache
    poisoning atau split-horizon DNS (perlu validasi dengan admin jaringan).
  common_causes:
    - "Malware yang modify DNS setting lokal (router, host file, atau adapter)"
    - "Compromised DNS resolver (ISP atau corporate)"
    - "Rogue DHCP server yang push DNS malicious"
    - "Man-in-the-Middle (MITM) attack di jaringan publik"
    - "Cache poisoning attack terhadap resolver upstream"
    - "Misconfig split-horizon DNS yang menampilkan internal site ke public"
  related_symptoms: [G24, G04, G21]
```

#### G24 — Hanya bisa akses via IP, bukan domain

- **short_desc:** Akses ke website via nama domain (mis. google.com) gagal/tidak sengaja redirect, tapi akses via IP langsung (mis. 142.250.193.78) berhasil. Indikasi masalah di layer DNS (P03 atau P04), bukan di layer koneksi/routing.
- **how_to_check:** `Jika domain gagal (timeout/redirect), coba akses via IP. Cara dapat IP resmi: nslookup <domain> 8.8.8.8 (DNS Google). Lalu ketik https://<IP> di browser. Jika berhasil → DNS issue (lihat P03/P04).`

```yaml
tutorial:
  definition: >
    Gejala "akses via IP works, via domain gagal" adalah signature problem
    DNS (P03 resolution failure atau P04 cache poisoning). Berbeda dari
    P01/P02 (tidak bisa koneksi sama sekali) — di P03/P04 network-layer
    masih OK (IP reachable), hanya name resolution yang bermasalah.
    Infoblox: "Cache poisoning is a more specific type of attack targeting
    caching name servers." Di P04, G24 hanya supporting karena signature
    kuat di P04 adalah redirect (G17); di P03 G24 adalah signature karena
    name resolution total gagal.
  verification_steps:
    - "Step 1: Identifikasi domain yang gagal (mis. google.com)."
    - "Step 2: Dapatkan IP resmi domain via DNS publik: jalankan `nslookup google.com 8.8.8.8` di CMD/Terminal."
    - "Step 3: Catat IP dari hasil (mis. 142.250.193.78)."
    - "Step 4: Buka browser, ketik `https://<IP>` (mis. https://142.250.193.78). Pakai https:// eksplisit."
    - "Step 5: Jika website muncul (mungkin dengan SSL warning karena cert tidak match IP) → konfirmasi DNS issue."
    - "Step 6: Untuk diferensiasi P03 vs P04 — coba nslookup domain (tanpa DNS Google). Jika timeout → P03. Jika return IP salah → P04 (poisoning)."
    - "Step 7: Sebagai sanity check, ping IP tersebut: `ping <IP>`. Jika ping OK tapi domain gagal → confirmed DNS layer problem."
  interpretation: >
    Domain & IP sama-sama gagal: P01/P02 (connectivity issue) | Domain
    gagal, IP works, nslookup timeout: P03 (DNS failure) | Domain redirect
    aneh, IP works, nslookup return IP salah: P04 (DNS poisoning) | Domain
    gagal, IP works, nslookup return IP benar tapi tetap gagal akses:
    kompleks, mungkin firewall aplikasi atau proxy.
  common_causes:
    - "DNS server tidak respond (P03)"
    - "DNS cache lokal corrupt atau dipoison (P04)"
    - "DNS setting adapter salah (kosong atau IP invalid)"
    - "Host file (Windows: C:\\Windows\\System32\\drivers\\etc\\hosts) di-modify malware"
    - "Split-horizon DNS yang salah konfigurasi"
  related_symptoms: [G17, G04, G21]
```

---

## P05 — DHCP Failure

**Kategori:** DHCP & IP Config
**Definisi:** Perangkat tidak mendapat IP address dari DHCP server, sehingga adapter memakai APIPA (169.254.x.x) atau tidak mendapat IP sama sekali. Penyebab tersering: DHCP server down, DHCP scope habis, port UDP 67/68 diblokir, atau kabel putus sehingga DHCP discovery gagal.
**Sumber utama riset:**

1. Microsoft Learn Q&A — "169.254 IP ADDRESS STUCK!" — https://learn.microsoft.com/en-us/answers/questions/3762106/169-254-ip-address-stuck
2. Spiceworks Community — "Laptop DHCP Issue: Automatically Assigning a 169.254.x.x IP Address" — https://community.spiceworks.com/t/laptop-dhcp-issue-automatically-assigning-a-169-254-x-x-ip-address/1237464
3. Quizlet — "Chapter 6: Supporting Network Services Flashcards" — https://quizlet.com/745442522/chapter-6-supporting-network-services-flash-cards/
4. Industrial Monitor Direct — "Fix 169.254.239.164 DHCP Failure - APIPA Address Resolution" — https://industrialmonitordirect.com/blogs/knowledgebase/resolving-169254xx-apipa-address-on-industrial-networks
5. Experts Exchange — "Event error DHCP server" — https://www.experts-exchange.com/questions/25060291/Event-error-DHCP-server.html
6. Ubiquiti Community — "Wireless DHCP Clients IP acquisition slow and unreliable, randomly getting 169.254" — https://community.ui.com/questions/Wireless-DHCP-Clients-IP-acquisition-slow-and-unreliable-randomly-getting-169-254-16-APIPA-addresse/c3c8a57f-58ff-4467-b30c-ee4011b57fb9

### Tabel CF_pakar

> Rule v1.0.0 berisi G05 + G30 + G40. Identitas P05 = DHCP acquisition failure → adapter fallback ke APIPA atau no IP.

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G05** | IP address 169.254.x.x (APIPA) | **0.95** | 0.9 (signature) | 0.9 → 0.95 (definitive OS-level indicator) | Definisi problem itu sendiri — APIPA adalah fallback Windows saat DHCP gagal. Microsoft Learn Q&A: *"An IP address that begins with 169.254 is called an APIPA address. It means that your computer cannot connect to your router."* Spiceworks, Industrial Monitor Direct, Ubiquiti — semua konsisten menyebut 169.254 sebagai signature DHCP failure. **Naik** ke 0.95 (bukan 0.9) karena definitive OS-level indicator — Windows sendiri yang menampilkan APIPA di ipconfig. Hampir tidak ada false positive (hanya saat user sengaja set static di range 169.254, sangat jarang). |
| 2 | **G30** | Device tidak mendapat IP DHCP | **0.85** | 0.9 (signature) | 0.9 → 0.85 (sedikit turun: general failure) | Common diagnostic indicator — `ipconfig` menampilkan IPv4 kosong atau 0.0.0.0. Quizlet (CompTIA Network+): soal klasik dengan jawaban APIPA untuk kasus ini. Industrial Monitor Direct: panduan ipconfig /release && /renew. **Turun** sedikit dari 0.9 ke 0.85 karena juga muncul saat user manually disable DHCP (static config yang salah) — bukan pure DHCP server failure. |
| 3 | **G40** | Error "Limited Connectivity" | **0.70** | 0.7 (common) | — | Common symptom Windows — muncul saat adapter punya IP tapi tidak bisa verify connectivity (gateway atau DNS unreachable). Quizlet: *"limited connectivity message and an address in the automatic IP addressing (APIPA) 169.254"* — berdekatan dengan G05. **Tidak dinaikkan** karena juga muncul di P02 (WAN down → adapter dapat IP LAN tapi "limited" ke internet), P03 (DNS gagal), atau P15 (router hang → sebagian client "limited"). Cross-cutting minor. |

### Evidence Summary

- **Definitive OS-level signature:** G05 (CF 0.95) — APIPA 169.254.x.x.
- **DHCP failure indicator:** G30 (CF 0.85) — no IP from DHCP.
- **Windows notification:** G40 (CF 0.7) — Limited Connectivity, cross-cutting.
- **Rule P05:** 3 gejala — lolos filter "≥ 2 gejala relevan" dengan kombinasi kaya.
- **Diferensiasi klinis:** G05 (APIPA) membedakan P05 dari P07 (dapat IP tapi subnet/gateway salah).

### Bundling Tutorial Gejala

#### G05 — IP address 169.254.x.x (APIPA)

- **short_desc:** Output `ipconfig` menampilkan IPv4 address berawalan 169.254 — Windows memberi APIPA (Automatic Private IP Addressing) karena gagal mendapat IP dari DHCP server dalam timeout (default ~60 detik).
- **how_to_check:** `Buka CMD → jalankan ipconfig → cari "IPv4 Address" di adapter Anda. Jika dimulai dengan 169.254 → G05 confirmed. APIPA range: 169.254.0.0 hingga 169.254.255.255.`

```yaml
tutorial:
  definition: >
    APIPA (Automatic Private IP Addressing) adalah mekanisme fallback
    Windows/Linux untuk memberi IP ke adapter saat DHCP gagal respond
    dalam ~60 detik. Range APIPA: 169.254.0.0/16 (169.254.0.0 hingga
    169.254.255.255). Microsoft Learn Q&A: "An IP address that begins
    with 169.254 is called an APIPA address. It means that your computer
    cannot connect to your router." Spiceworks: user report laptop dengan
    169.254 fix dengan unplug-replug ethernet. Industrial Monitor Direct:
    panduan lengkap release/renew. Konsekuensi: dengan APIPA, device hanya
    bisa communicate ke device lain APIPA di segment lokal — tidak bisa
    reach gateway, internet, atau device non-APIPA.
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Jalankan `ipconfig`. Cari adapter Anda (Ethernet atau WiFi)."
    - "Step 3: Lihat field `IPv4 Address`. Jika dimulai dengan 169.254.x.x → G05 confirmed."
    - "Step 4: Cek juga `Default Gateway`. Biasanya kosong atau tidak ada saat APIPA."
    - "Step 5: Test ping gateway (jika tahu gateway normal, mis. 192.168.1.1) — akan RTO karena APIPA di subnet berbeda."
    - "Step 6: Cek device lain di jaringan yang sama. Jika device lain juga 169.254 → DHCP server down (network-wide). Jika hanya 1 device → device-specific (cable, NIC, atau driver)."
    - "Step 7: Untuk fix — jalankan `ipconfig /release` lalu `ipconfig /renew` di CMD as admin. Tunggu 30 detik."
    - "Step 8: Jika masih 169.254 setelah renew — restart DHCP client service: buka Services (services.msc) → cari 'DHCP Client' → Restart."
    - "Step 9: Untuk konfirmasi server DHCP available — set static IP manual di range network (mis. 192.168.1.50), test ping gateway. Jika OK → DHCP server issue, bukan connectivity."
  interpretation: >
    169.254 + semua device: DHCP server down atau unreachable (P05
    network-wide) | 169.254 + hanya 1 device: kabel/NIC/driver device itu
    (device-specific) | 169.254 setelah renew: DHCP scope habis atau DHCP
    server config salah | Static IP works tapi DHCP gagal: confirmed DHCP
    server issue (bukan connectivity) | IPv4 kosong (no IP sama sekali):
    varian P05 — adapter bahkan tidak trigger APIPA.
  common_causes:
    - "DHCP server down (Windows Server, router DHCP service crash)"
    - "DHCP scope habis — semua IP sudah di-assign, tidak ada yang available (Industrial Monitor Direct)"
    - "Port UDP 67 atau 68 diblokir firewall atau ACL"
    - "Kabel putus sehingga DHCP discovery tidak reach server (lihat P14)"
    - "NIC driver corrupt — DHCP client service gagal"
    - "DHCP lease time terlalu panjang + device banyak → pool cepat habis"
    - "Rogue DHCP server memberikan IP dari pool salah (jarang menyebabkan 169.254 — biasanya dapat IP salah)"
  related_symptoms: [G30, G40, G01, G06]
```

#### G30 — Device tidak mendapat IP DHCP

- **short_desc:** `ipconfig` menampilkan IPv4 address kosong (tidak ada), atau "Media disconnected", padahal WiFi sudah connect / kabel sudah terpasang. Variant dari G05 — bahkan APIPA tidak diberikan.
- **how_to_check:** `Buka CMD → ipconfig → cari adapter Anda. Jika IPv4 Address kosong, atau hanya menampilkan 0.0.0.0 → G30. Test fix: ipconfig /release && ipconfig /renew.`

```yaml
tutorial:
  definition: >
    "Tidak dapat IP DHCP" adalah varian lebih parah dari G05 — adapter
    bahkan tidak trigger APIPA (mungkin karena DHCP client service crash
    di Windows, atau adapter belum selesai initialize). Quizlet (CompTIA
    Network+): soal klasik troubleshooting DHCP. Industrial Monitor
    Direct: panduan step-by-step release/renew. Berbeda dari G06 (IP
    conflict — dapat IP tapi duplikat) dan G07 (subnet/gateway salah —
    dapat IP tapi wrong config).
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Jalankan `ipconfig`. Cari adapter Anda (Ethernet atau WiFi)."
    - "Step 3: Lihat field `IPv4 Address`. Jika kosong, 0.0.0.0, atau tidak ada → G30."
    - "Step 4: Cek juga `Connection-specific DNS Suffix` — biasanya kosong saat DHCP gagal."
    - "Step 5: Cek status adapter di Network Connections (ncpa.cpl) — pastikan 'Enabled'."
    - "Step 6: Jalankan `ipconfig /release` (CMD as admin). Output harus konfirmasi release."
    - "Step 7: Lanjut `ipconfig /renew`. Tunggu 30-60 detik untuk DHCP discovery. Jika berhasil → akan ada IPv4 address baru."
    - "Step 8: Jika masih kosong — restart DHCP client service: buka Services.msc → cari 'DHCP Client' → Restart."
    - "Step 9: Cek juga 'Wired AutoConfig' dan 'WLAN AutoConfig' services — pastikan Running."
    - "Step 10: Jika DHCP dari router — cek router admin (http://192.168.1.1) → DHCP server setting. Pastikan enabled dan pool cukup besar."
  interpretation: >
    IPv4 kosong + semua device: DHCP server down (network-wide P05) |
    IPv4 kosong + hanya 1 device: adapter atau driver device itu |
    Release/renew berhasil: transient glitch solved | Release/renew gagal
    + semua device: DHCP server scope habis atau service crash | Static
    IP works tapi DHCP gagal: DHCP server issue confirmed | IPv4 muncul
    tapi 0.0.0.0: variant APIPA, kemungkinan TCP/IP stack corrupt.
  common_causes:
    - "DHCP client service Windows crash atau stopped (Industrial Monitor Direct)"
    - "TCP/IP stack corrupt — perlu netsh int ip reset"
    - "Adapter driver issue — gagal init DHCP discovery"
    - "DHCP server unreachable (down atau port UDP 67/68 blocked)"
    - "DHCP scope 100% utilized — pool habis"
    - "MAC address blacklist di DHCP server (rare)"
    - "Power management yang terlalu agresif — adapter di-disable saat idle, DHCP tidak reinit"
  related_symptoms: [G05, G40, G01, G20]
```

#### G40 — Error "Limited Connectivity"

- **short_desc:** Icon network di taskbar menampilkan segitiga kuning dengan tanda seru "!". Status connection: "Connected, no internet" atau "Limited". Berarti adapter punya IP (bukan APIPA) tapi Windows tidak bisa verify full connectivity ke gateway atau internet.
- **how_to_check:** `Hover icon network di taskbar → lihat status. Jika "No internet" atau "Limited" → G40. Konfirmasi: buka browser → coba website. Jika gagal tapi bisa ping gateway → G40.`

```yaml
tutorial:
  definition: >
    "Limited Connectivity" adalah alert Windows Network Awareness service
    saat adapter terhubung ke link-layer (WiFi atau Ethernet connect) tapi
    Windows tidak bisa confirm full network + internet connectivity.
    Quizlet: "limited connectivity message and an address in APIPA 169.254"
    — G40 sering muncul bersama G05. Tapi G40 juga muncul di banyak
    scenario lain: WAN down (P02), DNS gagal (P03), atau gateway
    unreachable. Berbeda dari APIPA — di G40 adapter biasanya sudah dapat
    IP valid (192.168.x.x) tapi connectivity limited.
  verification_steps:
    - "Step 1: Lihat icon network di taskbar. Segitiga kuning dengan tanda seru = limited/error."
    - "Step 2: Klik icon untuk lihat status. Catat teks: 'No internet', 'Limited', atau 'Connected, no internet'."
    - "Step 3: Buka CMD, jalankan `ipconfig`. Catat IPv4, gateway, DNS."
    - "Step 4: Jika IPv4 = 169.254.x.x → lihat G05 (DHCP failure)."
    - "Step 5: Jika IPv4 = 192.168.x.x valid → test ping gateway: `ping <gateway> -n 4`. Jika RTO → masalah gateway atau routing (lihat P07)."
    - "Step 6: Jika gateway OK → test ping 8.8.8.8. Jika RTO → WAN issue (lihat P02)."
    - "Step 7: Jika gateway OK dan 8.8.8.8 OK → test nslookup google.com. Jika gagal → DNS issue (lihat P03)."
    - "Step 8: Windows Network Awareness kadang tidak update langsung setelah problem solved. Jalankan `ipconfig /flushdns` dan tunggu 30 detik untuk status refresh."
    - "Step 9: Jika semua test OK tapi Windows masih tampilkan limited — restart Network Location Awareness service: Services.msc → 'Network Location Awareness' → Restart."
  interpretation: >
    G40 + IPv4 169.254: P05 (DHCP failure) | G40 + IPv4 valid + gateway
    RTO: P07 atau P01 (gateway issue) | G40 + IPv4 valid + gateway OK +
    internet RTO: P02 (WAN down) | G40 + IPv4 valid + gateway OK +
    internet OK + DNS gagal: P03 (DNS) | G40 + semua ping OK: Windows
    Network Awareness stale, restart service.
  common_causes:
    - "APIPA 169.254 (DHCP failure, G05)"
    - "Gateway unreachable (P07 atau P01)"
    - "WAN down (P02)"
    - "DNS failure (P03)"
    - "Windows Network Awareness service lag — perlu restart"
    - "Driver NIC bug yang salah report status ke Windows"
    - "MAC spoofing atau NAC yang block connectivity sementara"
  related_symptoms: [G05, G30, G01, G02, G03]
```

---

