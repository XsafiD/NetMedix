## P06 — IP Address Conflict

**Kategori:** DHCP & IP Config
**Definisi:** Dua atau lebih perangkat di jaringan menggunakan IP address yang sama — menyebabkan kedua device bermasalah (intermittent connectivity, ARP confusion). Biasanya terjadi saat static IP bentrok dengan DHCP pool, atau DHCP server memberikan IP duplikat (race condition).
**Sumber utama riset:**

1. ExpressVPN — "Windows has detected an IP address conflict: Fixed" — https://www.expressvpn.com/blog/windows-has-detected-ip-address-conflict/
2. DNSstuff — "IP Address Conflicts - Finding, Fixing, Avoiding [Guide]" — https://www.dnsstuff.com/ip-address-conflict
3. Microsoft Learn — "Event ID 4199 and Windows client can't get an IP address from the DHCP server" — https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/event-4199-windows-client-cannot-get-ip-address-dhcp-server
4. Cisco — "Troubleshoot 'Duplicate IP Address 0.0.0.0' Error Messages" — https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/8021x/116529-problemsolution-product-00.html
5. Spiceworks Community — "Windows has detected an IP address conflict" — https://community.spiceworks.com/t/windows-has-detected-an-ip-address-conflict/554945

### Tabel CF_pakar

> Rule v1.0.0 berisi G06 (CF 1.0 di MB-MD lama) + G23. Identitas P06 = Windows menampilkan pesan conflict (signature kuat, hampir definitive).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G06** | Pesan IP address conflict | **0.95** | 0.9 (signature) | 0.9 → 0.95 (definitive OS-level alert) | Definisi problem itu sendiri. Microsoft (Event ID 4199): *"Windows DHCP clients that obtain an IP address use a gratuitous ARP request to perform a client-based conflict detection before completing the address acquisition."* ExpressVPN: *"This message typically appears when the system detects a duplicate IPv4 assignment."* Cisco: dokumen troubleshoot spesifik untuk error ini. DNSstuff: panduan komprehensif. **Naik** ke 0.95 (bukan 0.9) karena ini OS-level alert definitive — sistem operasi sendiri yang mendeteksi (bukan user report). Hampir tidak ada false positive. |
| 2 | **G23** | Koneksi putus-nyala (intermittent) | **0.60** | 0.5 (supporting) | 0.5 → 0.6 (impact langsung dari ARP confusion) | Saat dua device pakai IP sama, ARP table bingung → traffic ke IP tsb kadang ke device A, kadang ke device B → koneksi terasa intermittent. Konsistensi dengan P11 (CF 0.6 — juga impact langsung dari packet loss). **Naik** dari 0.5 default karena di P06 G23 adalah mekanisme langsung (ARP flip-flop), bukan edge case seperti di P12 (CF 0.3). Cross-cutting tracking: G23 di P11=0.6, P06=0.6, P12=0.3 — konsisten dengan posisinya (impact langsung vs edge). |

### Evidence Summary

- **Signature symptom:** G06 (CF 0.95) — OS-level alert definitive.
- **Mechanism symptom:** G23 (CF 0.6) — ARP flip-flop dari dua device dengan IP sama.
- **Rule P06:** 2 gejala — lolos filter "≥ 2 gejala relevan".
- **Konsistensi cross-cutting:** G23 CF 0.6 sama dengan P11 (impact langsung), berbeda dari P12 (0.3, edge case).

### Bundling Tutorial Gejala

#### G06 — Pesan IP address conflict

- **short_desc:** Windows menampilkan popup/notifikasi "Windows has detected an IP address conflict" atau "Another computer on this network has the same IP address as this computer". Di Event Viewer muncul Event ID 4199.
- **how_to_check:** `Cek notifikasi Windows (kanan bawah) untuk pesan "IP address conflict". Buka Event Viewer → Windows Logs → System → filter Event ID 4199. Jalankan ipconfig — jika IP sama dengan device lain → conflict.`

```yaml
tutorial:
  definition: >
    IP address conflict terjadi saat dua device di jaringan yang sama
    menggunakan IPv4 address identik. Deteksi dilakukan oleh Windows via
    gratuitous ARP sebelum menyelesaikan DHCP acquisition (Microsoft
    Event ID 4199 docs). ExpressVPN: "typically appears when the system
    detects a duplicate IPv4 assignment." Mekanisme: device baru melakukan
    gratuitous ARP meng-claim IP X, tapi device existing sudah punya IP X
    → salah satu atau keduanya mendapat konflik warning. Impact: ARP
    table di switch/router bingung — traffic ke IP X bisa ke device A atau
    B secara random (flip-flop).
  verification_steps:
    - "Step 1: Cek system tray Windows (pojok kanan bawah) — cari notifikasi 'IP address conflict' atau segitiga kuning warning."
    - "Step 2: Buka Event Viewer (Win+R → ketik `eventvwr.msc` → Enter)."
    - "Step 3: Navigate ke Windows Logs → System. Klik kanan → Filter Current Log → ketik 4199 di field Event ID."
    - "Step 4: Jika ada event 4199 baru → confirmed IP conflict. Catat timestamp dan source (biasanya Tcpip)."
    - "Step 5: Buka CMD, jalankan `ipconfig` — catat IPv4 address device Anda (mis. 192.168.1.50)."
    - "Step 6: Cek device lain di jaringan — minta mereka juga `ipconfig`. Jika ada yang punya IP sama → confirmed."
    - "Step 7: Untuk deteksi silent conflict (tanpa warning Windows) — jalankan `arp -a` di CMD. Cek apakah ada MAC address berbeda untuk IP yang sama di entry berbeda (indikasi flip-flop)."
  interpretation: >
    Tidak ada notifikasi + tidak ada event 4199: tidak ada conflict |
    Notifikasi muncul tapi hilang setelah 1 menit: transient DHCP race,
    resolved otomatis | Event 4199 berulang: persistent conflict, perlu
    intervensi | IP device sama dengan IP device lain di jaringan:
    confirmed conflict, salah satu device harus release/renew.
  common_causes:
    - "Static IP manual di-set dalam range DHCP pool (DNSstuff — penyebab #1)"
    - "DHCP server memberikan IP duplikat akibat race condition atau database corrupt"
    - "Device resume dari sleep/hibernate dengan IP lama yang sudah di-assign ke device baru"
    - "DHCP pool terlalu kecil untuk jumlah device → collision probability naik"
    - "Rogue DHCP server di jaringan yang memberikan IP overlap"
    - "VPN client dengan IP lokal bentrok dengan IP LAN"
  related_symptoms: [G23, G05, G07]
```

#### G23 — Koneksi putus-nyala (intermittent)

> **Cross-reference:** Lihat bundling lengkap di P12. Di P06, G23 disebabkan ARP flip-flop saat dua device punya IP sama. CF_pakar 0.6 (impact langsung, konsisten dengan P11).

---

## P07 — Subnet Mask / Default Gateway Salah

**Kategori:** DHCP & IP Config
**Definisi:** Adapter dapat IP (bukan APIPA), tapi subnet mask atau default gateway salah — sehingga routing ke jaringan luar gagal. Penyebab tersering: manual misconfiguration (typo), DHCP server memberikan config salah, atau perubahan topologi jaringan belum di-update di device.
**Sumber utama riset:**

1. Extreme Networks — "Troubleshooting IP Default Gateway issues" — https://community.extremenetworks.com/t5/faqs/troubleshooting-ip-default-gateway-issues/td-p/44096
2. WikiHow — "Destination Host Unreachable: What Does It Mean in Ping?" — https://www.wikihow.com/Destination-Host-Unreachable
3. ArsTechnica — "Destination Host Unreachable no matter what I do...?" — https://arstechnica.com/civis/threads/destination-host-unreachable-no-matter-what-i-do.676056/
4. Cisco Community — "Destination Host Unreachable when trying to ping different computers" — https://community.cisco.com/t5/switching/destination-host-unreachable-when-trying-to-ping-different/td-p/4806949
5. SuperUser — "Why does ping return 'destination host unreachable' to the same subnet?" — https://superuser.com/questions/1706491/why-does-ping-return-destination-host-unreachable-to-the-same-subnet
6. Brother Support — "I am seeing a message, Destination Host Unreachable" — https://help.brother-usa.com/app/answers/detail/a_id/76187

### Tabel CF_pakar

> Rule v1.0.0 berisi G07 + G08 + G35. Identitas P07 = dapat IP valid tapi config salah → routing gagal.

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G08** | Tidak ada default gateway | **0.90** | 0.9 (signature) | — | Definisi problem — tanpa default gateway, device tidak bisa reach jaringan luar (routing table tidak punya entry default). Extreme Networks: troubleshooting guide spesifik untuk default gateway issue. WikiHow: panduan utama menyebut "incorrect default gateway" sebagai cause #1. Cisco & ArsTechnica: case studies gateway misconfig. Min 4 sumber. |
| 2 | **G35** | Error "Destination Host Unreachable" saat ping | **0.85** | 0.7 (common) | 0.7 → 0.85 (differentiator strong) | **Signature diagnostic** output ping. WikiHow: *"The majority of the time, 'destination host unreachable' is due to having the incorrect default gateway or subnet mask set."* Extreme Networks: *"A ping response of 'Destination Host Unreachable' is a solid indicator that there's a Default Gateway misconfiguration."* **Naik** ke 0.85 karena differentiator kuat — pesan spesifik ini (bukan RTO) menandakan routing/ARP problem, bukan connectivity loss. |
| 3 | **G07** | Subnet mask berbeda dari device lain | **0.80** | 0.7 (common) | 0.7 → 0.8 (differentiator strong) | Differentiator kuat — bandingkan subnet mask device bermasalah vs device normal. Jika berbeda → misconfiguration. SuperUser: diskusi subnet mismatch ARP resolution. Brother Support: troubleshooting subnet. **Naik** ke 0.8 karena differentiator kuat antara P07 vs P05/P06 — dapat IP tapi wrong mask. |

### Evidence Summary

- **Definitive config signature:** G08 (CF 0.9) — gateway kosong/0.0.0.0.
- **Diagnostic output signature:** G35 (CF 0.85) — "Destination Host Unreachable".
- **Differentiator vs other DHCP issues:** G07 (CF 0.8) — subnet mask beda.
- **Rule P07:** 3 gejala — lolos filter "≥ 2 gejala relevan" dengan kombinasi kaya.
- **Diferensiasi klinis:** P07 (dapat IP, wrong config) vs P05 (APIPA, no IP) vs P06 (IP valid, conflict).

### Bundling Tutorial Gejala

#### G07 — Subnet mask berbeda dari device lain

- **short_desc:** Subnet mask di adapter Anda berbeda dengan subnet mask device lain di jaringan yang sama (mis. Anda 255.255.255.128, semua device lain 255.255.255.0). Akibatnya, ARP resolution gagal untuk device di luar subnet yang Anda anggap.
- **how_to_check:** `Buka CMD → ipconfig → catat "Subnet Mask" di adapter Anda. Bandingkan dengan device lain di jaringan (jalan ipconfig di device lain). Jika berbeda → G07. Cek juga apakah bisa ping device lain di subnet lokal.`

```yaml
tutorial:
  definition: >
    Subnet mask menentukan size network local dan bagaimana IP address
    di-split antara network/host portion. Mismatch subnet mask antara
    device di jaringan yang sama → ARP resolution gagal → "Destination
    Host Unreachable" (G35). SuperUser: diskusi ARP failure saat subnet
    mask mismatch. Common scenario: device A manual config dengan subnet
    /24 (255.255.255.0), device B dengan /25 (255.255.255.128) — device B
    tidak bisa reach device di host range 128-254. Brother Support:
    printer network troubleshooting subnet check.
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Jalankan `ipconfig`. Catat `Subnet Mask` di adapter Anda (mis. 255.255.255.0)."
    - "Step 3: Bandingkan dengan device lain di jaringan yang sama (HP, tablet, laptop kedua) — minta mereka juga `ipconfig` (di Windows) atau cek Settings → Network."
    - "Step 4: Catat subnet mask device lain. Jika berbeda dengan device Anda → G07 confirmed."
    - "Step 5: Test ping device lain di subnet lokal: `ping <IP-device-lain>`. Jika gagal dengan 'Destination Host Unreachable' (G35) → konfirmasi P07."
    - "Step 6: Test ping gateway: `ping <gateway>`. Jika gateway di subnet berbeda dari Anda (mis. Anda 192.168.1.50/24, gateway 192.168.1.1) — harusnya OK. Jika gateway di luar subnet Anda → G07 confirmed."
    - "Step 7: Untuk fix — ubah ke DHCP: Settings → Network → adapter Properties → IPv4 → Obtain an IP address automatically."
    - "Step 8: Atau set static dengan config yang benar — pakai subnet mask yang sama dengan device lain (biasanya 255.255.255.0 untuk home network)."
  interpretation: >
    Subnet mask sama dengan semua device: tidak ada G07 → lihat gejala
    lain | Subnet mask beda dari device lain: confirmed G07 (P07) |
    Ping device lokal OK tapi gateway/internet gagal: gateway di subnet
    berbeda atau default route missing | Setelah fix subnet mask semua
    ping OK: confirmed subnet mask adalah cause.
  common_causes:
    - "Manual typo saat set static IP (lupa ganti subnet mask)"
    - "DHCP server memberikan subnet mask salah"
    - "Topologi jaringan diubah (mis. split jaringan jadi VLAN) tapi config device lama masih pakai subnet mask lama"
    - "VPN client yang override adapter setting dengan subnet lokal VPN"
    - "Profile network corrupt di Windows"
    - "Salin-paste config dari network lain tanpa adjust"
  related_symptoms: [G08, G35, G05, G06]
```

#### G08 — Tidak ada default gateway

- **short_desc:** Output `ipconfig` menampilkan "Default Gateway" kosong atau 0.0.0.0. Tanpa default gateway, device tidak tahu kemana mengirim traffic ke jaringan luar (internet, atau subnet lain).
- **how_to_check:** `Buka CMD → ipconfig /all → cari "Default Gateway" di adapter Anda. Jika kosong atau 0.0.0.0 → G08. Test ping IP luar subnet (mis. 8.8.8.8) — akan muncul "Destination Host Unreachable" atau "General failure".`

```yaml
tutorial:
  definition: >
    Default gateway adalah entry routing table default — kemana device
    mengirim traffic kalau destination IP tidak di subnet lokal. Tanpa
    default gateway, device hanya bisa communicate ke IP di subnet lokal
    yang sama. Extreme Networks: troubleshooting guide spesifik untuk
    default gateway issue. WikiHow: penyebab #1 "Destination Host
    Unreachable". Penting: di DHCP config, gateway otomatis diberikan
    (DHCP option 3). G08 terjadi saat DHCP gagal give gateway, atau saat
    static config tanpa gateway diisi.
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Jalankan `ipconfig /all`. Cari adapter Anda (Ethernet atau WiFi)."
    - "Step 3: Lihat field `Default Gateway`. Jika kosong, 0.0.0.0, atau tidak ada → G08 confirmed."
    - "Step 4: Catat IPv4 address dan subnet mask Anda (mis. 192.168.1.50, 255.255.255.0). Gateway normal untuk subnet ini: 192.168.1.1."
    - "Step 5: Test ping IP luar subnet (mis. 8.8.8.8). Jika muncul 'Destination Host Unreachable' atau 'General failure' → konfirmasi no default route."
    - "Step 6: Cek routing table: `route print` di CMD. Cari entry dengan `Network Destination` = 0.0.0.0 dan `Netmask` = 0.0.0.0 — ini default route. Jika tidak ada → confirmed G08."
    - "Step 7: Test ping IP di subnet lokal (mis. 192.168.1.X device lain) — harusnya OK walau gateway missing (only affects routing luar)."
    - "Step 8: Untuk fix — ganti ke DHCP: Settings → Network → adapter Properties → IPv4 → Obtain an IP address automatically."
    - "Step 9: Atau set static dengan gateway benar: Use the following IP address → Default Gateway = 192.168.1.1 (sesuaikan dengan jaringan Anda)."
  interpretation: >
    Gateway kosong + semua ping gagal termasuk lokal: juga P01 (NIC
    issue) | Gateway kosong + ping lokal OK + ping luar "Destination Host
    Unreachable": confirmed G08 (P07) | Gateway 0.0.0.0: adapter tidak
    dapat gateway dari DHCP, kemungkinan DHCP option 3 missing di server
    | Setelah fix gateway, semua ping OK: confirmed gateway adalah cause.
  common_causes:
    - "DHCP server tidak memberikan gateway (DHCP option 3 missing)"
    - "Static config salah — user tidak mengisi field gateway"
    - "VPN client yang override gateway lokal dengan gateway VPN yang invalid"
    - "TCP/IP stack corrupt — perlu netsh int ip reset"
    - "DHCP client service gagal register gateway ke adapter"
    - "Multiple adapter di device — gateway hanya set di satu, yang aktif tidak"
  related_symptoms: [G07, G35, G05, G01]
```

#### G35 — Error "Destination Host Unreachable" saat ping

- **short_desc:** Output ping menampilkan "Reply from <IP-anda>: Destination host unreachable" atau "Destination Net Unreachable" — berarti device Anda (atau router) tidak tahu kemana mengirim paket ke destination. Berbeda dari RTO (Request Timed Out — destination tahu tapi tidak respond).
- **how_to_check:** `Buka CMD → ping <destination> -n 4. Baca output. Jika "Destination host unreachable" atau "Destination net unreachable" → G35. Bedakan dari "Request timed out" (RTO, different cause).`

```yaml
tutorial:
  definition: >
    "Destination Host Unreachable" adalah ICMP error message yang dikirim
    oleh router atau local stack saat tidak ada route ke destination.
    WikiHow: "The majority of the time, 'destination host unreachable'
    is due to having the incorrect default gateway or subnet mask set."
    Extreme Networks: "solid indicator of Default Gateway misconfiguration."
    SuperUser: diskusi ARP failure untuk same-subnet unreachable. Berbeda
    dari RTO (Request Timed Out — destination reachable tapi tidak
    respond, indikasi firewall atau packet loss). Mekanisme unreachable:
    1) device cek routing table → no route → local stack generate ICMP
    unreachable; atau 2) router forward paket tapi next-hop tidak ada →
    router generate ICMP unreachable.
  verification_steps:
    - "Step 1: Buka CMD (Win+R → cmd → Enter)."
    - "Step 2: Jalankan ping dengan target: `ping <destination-IP> -n 4`. Destination bisa domain atau IP."
    - "Step 3: Baca output dengan teliti. Bedakan tiga jenis error: 'Request timed out' (RTO, target reachable tapi tidak respond) | 'Destination host unreachable' (G35, no route ke target) | 'PING: transmit failed. General failure' (stack/NIC issue)."
    - "Step 4: Jika G35 — cek source IP di reply. 'Reply from <IP-anda>' berarti local stack yang generate (no route di routing table Anda). 'Reply from <router-IP>' berarti router yang generate (router tidak tahu next-hop)."
    - "Step 5: Cek ipconfig — pastikan Default Gateway terisi (G08) dan Subnet Mask benar (G07)."
    - "Step 6: Cek routing table: `route print`. Cari entry default (0.0.0.0 → gateway). Jika tidak ada → confirmed G08."
    - "Step 7: Clear ARP cache: `arp -d *` di CMD as admin. Kadang ARP table corrupt menyebabkan unreachable untuk same-subnet."
    - "Step 8: Test ping ke IP lokal yang diketahui aktif (mis. 192.168.1.X device lain). Jika juga unreachable → subnet mask atau ARP issue."
    - "Step 9: Untuk fix — set DHCP otomatis: Settings → Network → adapter Properties → IPv4 → Obtain an IP address automatically. Atau fix static config dengan gateway dan subnet mask benar."
  interpretation: >
    'Reply from <IP-anda>: Destination host unreachable': routing table
    lokal tidak punya route → G08 (P07) | 'Reply from <router-IP>:
    Destination net unreachable': router tidak tahu next-hop → routing
    upstream issue | Unreachable untuk same-subnet: subnet mask mismatch
    (G07) atau ARP cache corrupt | RTO bukan unreachable: destination
    reachable tapi tidak respond, indikasi P11 (loss) atau P13 (firewall)
    | General failure: NIC/stack issue, lihat P01.
  common_causes:
    - "Default gateway kosong atau salah (G08, P07)"
    - "Subnet mask salah — device anggap destination di luar subnet padahal dalam (G07)"
    - "Routing table corrupt atau tidak ada default route"
    - "ARP cache corrupt — entry MAC untuk IP hilang atau salah"
    - "Router upstream tidak punya route ke destination (jarang di internet publik)"
    - "VPN client yang inject route salah ke routing table"
  related_symptoms: [G07, G08, G01, G03]
```

---

## P08 — Tidak Bisa Connect ke WiFi

**Kategori:** WiFi
**Definisi:** Perangkat gagal terhubung ke jaringan WiFi sama sekali — entah SSID tidak muncul di daftar, atau muncul tapi proses connect gagal/tidak bisa authenticate. Berbeda dari P09 (signal lemah — connect berhasil tapi throughput rendah) dan P01 (no connectivity — bisa connect WiFi tapi tidak ada network).
**Sumber utama riset:**

1. Microsoft Support — "Fix Wi-Fi connection issues in Windows" — https://support.microsoft.com/en-us/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows
2. Microsoft Learn — "Connecting to a hidden WiFi network" (Linksys) — https://support.linksys.com/kb/article/515-en/
3. Microsoft Learn Q&A — "My PC only shows my network as 'Hidden Network'" — https://learn.microsoft.com/en-us/answers/questions/4063578/my-pc-only-shows-my-network-as-hidden-network-and
4. Ubiquiti Community — "Devices unable to connect when SSID is hidden" — https://community.ui.com/questions/devices-unable-to-connect-when-SSID-is-hidden/26a038a6-3e7e-4bb5-ba37-e1f553708ff0
5. SuperUser — "Windows 10 Can't Connect to Hidden Network on Boot" — https://superuser.com/questions/1144806/windows-10-cant-connect-to-hidden-network-on-boot
6. MakeUseOf — "How to Fix 'You Are Not Connected to Any Networks' on Windows" — https://www.makeuseof.com/not-connected-any-networks-error-windows/

### Tabel CF_pakar

> Rule v1.0.0 berisi G09 + G10. Identitas P08 = failure di tahap connection establishment (auth, association) — berbeda dari P09 (signal lemah, established tapi throughput rendah).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G09** | Tidak bisa connect ke WiFi | **0.85** | 0.9 (signature) | 0.9 → 0.85 (sedikit turun: failure mode general) | Definisi problem itu sendiri — failure untuk establish connection. Microsoft Support: panduan comprehensive untuk "fix Wi-Fi connection issues" dengan G09 sebagai primary symptom. Ubiquiti, Linksys, MakeUseOf — semua memakai G09 sebagai entry point diagnostik. **Turun** sedikit dari 0.9 ke 0.85 karena "tidak bisa connect" adalah failure mode general yang juga bisa muncul di P01 (NIC disabled → tidak bisa connect WiFi), P05 (DHCP gagal → connect tapi no IP), P13 (firewall blok). Cross-cutting minor. |
| 2 | **G10** | SSID WiFi tidak muncul | **0.80** | 0.7 (common) | 0.7 → 0.8 (differentiator strong) | Differentiator kuat antara P08 (problem di sisi client/SSID visibility) vs P09 (SSID muncul tapi signal lemah). Microsoft: *"If your wireless network adapter isn't listed in Device Manager, then Windows doesn't detect it."* Linksys & Ubiquiti: hidden SSID adalah cause specifik. SuperUser: Windows 10 hidden network boot issue. **Naik** ke 0.8 karena differentiator — jika SSID tidak muncul, scope problem menyempit (driver WiFi, hidden SSID, atau band incompatible). |

### Evidence Summary

- **Primary symptom:** G09 (CF 0.85) — failure connect, sedikit turun karena general failure mode.
- **Differentiator symptom:** G10 (CF 0.8) — SSID tidak muncul, differentiator dari P09.
- **Rule P08:** 2 gejala — lolos filter "≥ 2 gejala relevan".
- **Diferensiasi klinis:** G10 (SSID tidak muncul) menandai P08 (connection establishment failure) vs P09 (signal bar 1-2 = connect berhasil tapi lemah).

### Bundling Tutorial Gejala

#### G09 — Tidak bisa connect ke WiFi

- **short_desc:** Perangkat gagal melakukan connect ke WiFi — bisa karena password salah, authentication timeout, association failure, atau adapter issue. Tanda: klik connect → "Can't connect to this network" atau spinning lalu gagal.
- **how_to_check:** `Klik icon WiFi di taskbar → pilih SSID → klik Connect → masukkan password. Jika muncul "Can't connect to this network" atau spinning berlama-lama lalu gagal → G09. Coba juga: forget network lalu reconnect, restart WiFi adapter, atau coba dari device lain untuk isolasi.`

```yaml
tutorial:
  definition: >
    "Tidak bisa connect WiFi" berarti proses establishment koneksi WiFi
    gagal di salah satu tahap: scan (SSID tidak ditemukan), auth (password
    salah atau security mode mismatch), association (AP reject), atau DHCP
    (no IP setelah association). Microsoft Support mengelompokkan root
    cause: adapter disabled, driver outdated, password salah, security
    mode (WPA2/WPA3) incompatible, atau hidden SSID. Penting: berbeda
    dari P09 (connect berhasil tapi signal 1-2 bar) dan P01 (connect
    berhasil tapi tidak ada network connectivity).
  verification_steps:
    - "Step 1: Klik icon WiFi di taskbar Windows (pojok kanan bawah). Pastikan WiFi toggle ON."
    - "Step 2: Identifikasi SSID target di daftar jaringan. Jika tidak ada → lihat G10."
    - "Step 3: Klik SSID → klik Connect. Masukkan password yang benar (cek capslock, gunakan show password)."
    - "Step 4: Amati hasil: 'Connected, secured' = sukses | 'Can't connect to this network' = G09 | spinning lalu gagal = G09 | 'No internet, secured' = connect OK tapi DHCP/WAN issue (lihat P05/P02)."
    - "Step 5: Jika gagal, klik kanan SSID → Forget. Lalu coba Connect ulang dengan password benar."
    - "Step 6: Restart WiFi adapter: Settings → Network & Internet → Advanced network settings → Wi-Fi → Disable, tunggu 10 detik, Enable."
    - "Step 7: Test dari device lain (HP, tablet) ke SSID yang sama. Jika semua device gagal → masalah di router/AP (lihat P15). Jika hanya 1 device → masalah adapter/driver."
    - "Step 8: Update driver WiFi: Device Manager → Network adapters → right-click WiFi adapter → Update driver → Search automatically."
  interpretation: >
    Connect berhasil di device lain: masalah adapter/driver device ini |
    Connect gagal di semua device: masalah router/AP (P15) atau security
    mode incompatible | "Can't connect" setelah forget+reconnect: password
    salah atau security mode mismatch (WPA3 vs WPA2) | Spinning berlama-lama
    lalu gagal: association timeout, kemungkinan AP overload atau band
    mismatch (6GHz client vs 2.4GHz-only AP).
  common_causes:
    - "Password salah (typo, capslock, atau password router baru setelah reboot)"
    - "Security mode tidak kompatibel (WPA3-only client vs WPA2-only AP, atau sebaliknya)"
    - "Hidden SSID — perlu manual connect (Linksys, Ubiquiti)"
    - "Driver WiFi outdated atau corrupt (Microsoft Support)"
    - "WiFi adapter disabled secara software (Airplane mode, Fn-key)"
    - "Band tidak kompatibel (client 2.4GHz-only vs AP 5GHz-only, atau 6GHz)"
    - "MAC filtering di router yang block device"
    - "AP overload — terlalu banyak client connect"
  related_symptoms: [G10, G11, G36, G37]
```

#### G10 — SSID WiFi tidak muncul

- **short_desc:** Saat membuka daftar WiFi (klik icon WiFi di taskbar), SSID target tidak ada di list — padahal device lain di lokasi yang sama bisa melihatnya, atau router diketahui aktif.
- **how_to_check:** `Klik icon WiFi di taskbar → lihat daftar SSID. Jika SSID target tidak ada → G10. Coba: scroll daftar, tunggu 30 detik (scan ulang), atau coba di device lain. Jika device lain bisa lihat → masalah receiver device ini.`

```yaml
tutorial:
  definition: >
    SSID tidak muncul menandakan masalah di tahap scan/probe — bukan auth.
    Microsoft Learn Q&A: user report "My PC only shows my network as
    'Hidden Network' and won't connect" — klasik untuk SSID hidden atau
    band incompatible. Microsoft Support: "If your wireless network
    adapter isn't listed in Device Manager, then Windows doesn't detect
    it." Ubiquiti: hidden SSID sering bermasalah di sebagian device.
    Differentiator dari P09 (SSID muncul tapi 1-2 bar).
  verification_steps:
    - "Step 1: Klik icon WiFi di taskbar. Tunggu 30 detik agar scan selesai."
    - "Step 2: Scroll daftar SSID sampai bawah. Cari SSID target. Jika tidak ada → lanjut."
    - "Step 3: Cek device lain (HP/tablet/laptop kedua) di lokasi yang sama. Jika device lain bisa lihat SSID → masalah receiver device ini (driver, band)."
    - "Step 4: Jika semua device tidak bisa lihat SSID → masalah router/AP: hidden SSID, atau SSID sengaja disabled, atau AP mati."
    - "Step 5: Untuk konfirmasi hidden SSID — coba connect manual: Settings → Network & Internet → Wi-Fi → Manage known networks → Add network → ketik SSID eksak."
    - "Step 6: Cek band adapter: Device Manager → Network adapters → right-click WiFi → Properties → Advanced → lihat 'Wireless Mode'. Pastikan support 802.11b/g/n (2.4GHz) dan 802.11a/ac/ax (5GHz)."
    - "Step 7: Update driver WiFi (Device Manager → Update driver). Driver lama sering gagal detect SSID tertentu."
    - "Step 8: Restart WiFi service: buka CMD as admin → `netsh winsock reset` lalu `netsh int ip reset` → restart Windows."
  interpretation: >
    SSID muncul di device lain: masalah receiver/driver device ini | SSID
    tidak muncul di semua device: hidden SSID, atau AP mati/misconfig |
    SSID muncul setelah manual add: confirmed hidden SSID | SSID hanya
    muncul setelah driver update: driver issue | SSID tidak muncul setelah
    reset network: kemungkinan adapter hardware rusak.
  common_causes:
    - "SSID disembunyikan (hidden) di setting router (Linksys, Ubiquiti)"
    - "Driver WiFi outdated — gagal detect band atau protocol tertentu (Microsoft)"
    - "Band mismatch — AP 5GHz-only, client 2.4GHz-only (atau 6GHz)"
    - "Adapter WiFi disabled di Device Manager atau Fn-key"
    - "WiFi service Windows crashed — perlu restart service"
    - "Channel WiFi tidak standar (mis. channel 13/14 yang tidak didukung US device)"
    - "AP mati atau boot loop (lihat P15)"
  related_symptoms: [G09, G11, G36, G37]
```

---

## P09 — WiFi Signal Lemah / Interferensi

**Kategori:** WiFi
**Definisi:** WiFi connect berhasil, tapi signal sangat lemah (1-2 bar) atau sering disconnect karena jarak AP terlalu jauh, hambatan fisik (dinding, microwave), atau interferensi channel (terutama 2.4GHz crowded). Berbeda dari P08 (tidak bisa connect sama sekali) — di P09 association berhasil, hanya throughput/stabilitas yang terdampak.
**Sumber utama riset:**

1. AT&T — "Wi-Fi Interference: 7 Things That Block Wi-Fi Signal" — https://www.att.com/internet/wifi-interference-things-that-block-wifi-signals/
2. EPB — "WiFi Keeps Disconnecting? Quick Fixes to Try First" — https://epb.com/get-connected/tech-support/how-to-stop-wifi-from-disconnecting/
3. Cisco Community — "Why are devices on 2.4GHz constantly disconnecting?" — https://community.cisco.com/t5/wireless/why-are-devices-on-2-4ghz-constantly-disconnecting-and/td-p/5521918
4. Netgear Community — "2.4GHz stops working" — https://community.netgear.com/discussions/home-wifi-routers-nighthawk/2-4ghz-stops-working/494947
5. Microsoft Learn Q&A — "Why is my Wifi often slow and cutting out on only one device?" — https://learn.microsoft.com/en-us/answers/questions/4011191/why-is-my-wifi-often-slow-and-cutting-out-on-only
6. Google Help (Pixel) — "Having issues when connected to 5GHz wifi network" — https://support.google.com/pixelphone/thread/207536043

### Tabel CF_pakar

> Rule v1.0.0 berisi G11 + G12. Identitas P09 = connect berhasil tapi signal/throughput buruk — berbeda dari P08 (gagal connect total).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G11** | WiFi signal bar 1-2 | **0.90** | 0.9 (signature) | — | Signature symptom P09 — definisi "signal lemah" itu sendiri. AT&T: *"Since 2.4 GHz frequency travels further, devices on the 2.4 GHz band are more susceptible to Wi-Fi interference than devices operating on the 5 GHz band."* Microsoft Learn Q&A: *"Check for Interference and Signal Strength. Change WiFi Channel and Frequency."* EPB & Cisco Community — semua konsisten memakai signal strength sebagai primary diagnostic. Min 4 sumber. |
| 2 | **G12** | WiFi sering disconnect | **0.70** | 0.7 (common) | — | Common symptom dari signal parah atau interference parah. EPB: *"Step 1: Reboot Your Router · Step 4: The Router Is in a Bad Spot · Step 3: You're Getting Radio Interference."* Cisco Community: 2.4GHz disconnect karena channel settings atau client balancing. Netgear Community: 2.4GHz stops working issue. **Tidak dinaikkan** (tetap 0.7) karena juga bisa muncul di P11 (packet loss menyebabkan WiFi terasa disconnect), P15 (router hang), P12 (latency ekstrim). Cross-cutting minor. |

### Evidence Summary

- **Signature symptom:** G11 (CF 0.9) — signal bar rendah adalah definisi P09.
- **Common symptom:** G12 (CF 0.7) — disconnect, cross-cutting minor dengan P11/P15/P12.
- **Rule P09:** 2 gejala — lolos filter "≥ 2 gejala relevan".
- **Diferensiasi klinis:** G11 membedakan P09 (signal lemah) dari P08 (tidak connect sama sekali → no signal info).

### Bundling Tutorial Gejala

#### G11 — WiFi signal bar 1-2

- **short_desc:** Indikator signal WiFi di taskbar/device hanya menampilkan 1-2 bar (dari 4 atau 5). Connection established tapi throughput rendah, latency tinggi, dan mudah drop.
- **how_to_check:** `Lihat icon WiFi di taskbar Windows/Android/iOS. Hitung bar signal. 1-2 bar = G11 (signal lemah). Untuk angka presisi (dBm): gunakan WiFi Analyzer (Android) atau `netsh wlan show interfaces` di Windows CMD. Idealnya > -65 dBm.`

```yaml
tutorial:
  definition: >
    Signal WiFi diukur dalam dBm (decibel-milliwatt) — semakin dekat ke 0
    semakin kuat. Range typical: -30 dBm (excellent, bersebelahan AP)
    hingga -90 dBm (unusable). Threshold umum: >-50 excellent, -50 to -65
    good, -65 to -75 fair (1-2 bar), <-85 unusable. AT&T: 2.4GHz lebih
    jangkauan tapi lebih rentan interference; 5GHz lebih cepat tapi
    shorter range. EPB: "The Router Is in a Bad Spot" + "You're Getting
    Radio Interference" — dua penyebab utama signal lemah.
  verification_steps:
    - "Step 1: Lihat icon WiFi di taskbar Windows. Hitung bar: 4 bar = excellent, 3 = good, 2 = fair, 1 = poor, 0 = no signal."
    - "Step 2: Untuk pengukuran presisi — install WiFi Analyzer (Microsoft Store) atau acrylic WiFi. Atau jalankan `netsh wlan show interfaces` di CMD dan lihat field `Signal` (dalam %)."
    - "Step 3: Untuk angka dBm: gunakan WiFi Analyzer Android atau `iwconfig` di Linux. Catat nilai `link level` (mis. -75 dBm)."
    - "Step 4: Berjalan mendekati router/AP — cek apakah signal naik ke 3-4 bar. Jika ya → jarak/hambatan adalah cause."
    - "Step 5: Cek channel WiFi via WiFi Analyzer — jika banyak SSID tetangga di channel yang sama → interference (co-channel)."
    - "Step 6: Test apakah device lain di lokasi yang sama juga 1-2 bar. Jika ya → environment issue, bukan device-specific."
    - "Step 7: Cek band — jika connect ke 5GHz di jarak jauh, signal akan drop cepat (5GHz range lebih pendek). Coba switch ke 2.4GHz untuk range."
    - "Step 8: Untuk konfirmasi interferensi non-WiFi — matikan sementara microwave, bluetooth device, cordless phone 2.4GHz, atau baby monitor. Cek apakah signal membaik."
  interpretation: >
    4 bar (> -50 dBm): excellent | 3 bar (-50 to -65): good, normal | 2 bar
    (-65 to -75): fair, throughput mulai turun untuk real-time apps | 1 bar
    (-75 to -85): poor, disconnect probable | 0 bar (< -85 dBm): unusable.
  common_causes:
    - "Jarak AP terlalu jauh (signal attenuation free-space)"
    - "Hambatan fisik — dinding beton, lantai metal, cermin (AT&T)"
    - "Interferensi co-channel — banyak SSID di channel yang sama (Cisco Community)"
    - "Interferensi non-WiFi — microwave 2.4GHz, bluetooth, cordless phone, baby monitor"
    - "Band tidak optimal — 5GHz di jarak jauh (lebih cepat tapi range pendek)"
    - "AP placement buruk — di pojok rumah, di belakang TV metal, di lantai (EPB)"
    - "Antena AP rusak atau orientasi horizontal vs vertical mismatch"
  related_symptoms: [G12, G13, G15, G09]
```

#### G12 — WiFi sering disconnect

- **short_desc:** Perangkat terus-menerus disconnect dari WiFi secara spontan — beberapa menit connect, lalu drop, lalu reconnect. Cycle berulang. Berbeda dari P11 (intermittent di semua koneksi), P09 ini spesifik ke WiFi link-level disconnect.
- **how_to_check:** `Amati icon WiFi di taskbar selama 10-30 menit. Jika berubah dari connected → not connected secara periodik → G12. Cek Event Viewer → Windows Logs → System → filter "WLAN-AutoConfig" (Event ID 8000/8001) untuk log disconnect.`

```yaml
tutorial:
  definition: >
    WiFi disconnect berulang adalah symptom link-layer instability —
    berbeda dari packet loss (P11, network-layer) atau internet drop
    (P02, WAN-side). EPB: "WiFi Keeps Disconnecting — Quick Fixes to Try
    First": reboot router, update firmware, radio interference, router
    placement. Cisco Community: 2.4GHz disconnect karena channel settings,
    client balancing, atau band steering. Netgear: 2.4GHz stops working
    issue — spesifik ke band 2.4GHz.
  verification_steps:
    - "Step 1: Amati icon WiFi di taskbar selama 10-30 menit. Hitung berapa kali disconnect terjadi."
    - "Step 2: Buka Event Viewer → Windows Logs → System. Filter event source 'WLAN-AutoConfig'."
    - "Step 3: Cari Event ID 8001 (disconnect) dan 8000 (connect). Catat timestamp — pola periodik?"
    - "Step 4: Cek signal bar saat disconnect terakhir — jika 1-2 bar sebelum disconnect → signal too weak (P09)."
    - "Step 5: Cek apakah disconnect terjadi saat device idle (power saving issue) atau aktif (interference/congestion)."
    - "Step 6: Untuk isolasi device-specific vs AP-specific — test device lain di lokasi yang sama. Jika hanya 1 device → driver/power setting. Jika semua → AP/environment."
    - "Step 7: Cek power management WiFi: Device Manager → WiFi adapter → Properties → Power Management → uncheck 'Allow computer to turn off this device'."
    - "Step 8: Update driver WiFi dan firmware router. Driver lama sering menyebabkan disconnect intermittent."
  interpretation: >
    Disconnect tiap 1-5 menit: signal parah atau interference berat |
    Disconnect tiap 10-30 menit saat idle: power saving issue | Disconnect
    saat ada activity (download besar): AP overload atau QoS drop |
    Disconnect semua device di rumah: AP/router issue (P15) | Disconnect
    satu device saja: adapter driver atau power setting.
  common_causes:
    - "Signal terlalu lemah → auto-disconnect threshold tercapai (lihat G11)"
    - "Power management WiFi terlalu agresif (Windows turn off adapter saat idle)"
    - "Driver WiFi outdated atau buggy"
    - "Channel interference parah (Cisco Community, Netgear)"
    - "AP firmware buggy — perlu update (EPB)"
    - "Band steering AP terlalu agresif (kick client dari 5GHz ke 2.4GHz)"
    - "Client balancing multi-AP yang salah konfigurasi (Cisco)"
    - "Overheating AP yang merestart WiFi radio sendiri"
  related_symptoms: [G11, G13, G15, G23]
```

---

## P10 — Jaringan Lambat / Bandwidth Saturation

**Kategori:** Performa
**Definisi:** Kecepatan internet/jaringan jauh di bawah paket ISP atau ekspektasi baseline. Bisa disebabkan bandwidth saturation (banyak user/device share koneksi), QoS misconfig, background download besar, atau ISP throttling. Berbeda dari P11 (packet loss) dan P12 (latensi) — di P10 indikator utama adalah throughput Mbps rendah.
**Sumber utama riset:**

1. PingPlotter — "Find The Device Slowing Down Your Network (Hidden Bandwidth Saturation Sources)" — https://www.pingplotter.com/wisdom/article/hidden-bandwidth-saturation-sources/
2. Sonic Internet — "Bandwidth Saturation" — https://help.sonic.com/hc/en-us/articles/115010633068-Bandwidth-Saturation
3. Endace — "Troubleshoot Network Quality of Service (QoS)" — https://www.endace.com/solutions/network-performance-monitoring/network-quality-of-service-troubleshooting
4. Cisco Community — "QoS troubleshooting" — https://community.cisco.com/t5/network-management/qos-troubleshooting/td-p/3059621
5. Network Journey — "QoS Diagnose & Fix Network Performance Issues" — https://networkjourney.com/qos-diagnose-fix-network-performance-issues-ccnp-enterprise/
6. Intermedia — "Quality Of Service (QoS) Troubleshooting" — https://support.intermedia.com/app/articles/detail/a_id/11982/~/quality-of-service-%2528qos%2529-troubleshooting

### Tabel CF_pakar

> Rule v1.0.0 berisi G13 + G22. Identitas P10 = throughput rendah (Mbps) — berbeda dari P11 (loss) dan P12 (latency).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G22** | Speed test hasil sangat rendah | **0.90** | 0.9 (signature) | — | Signature symptom — definisi throughput problem itu sendiri. Sonic: *"Bandwidth saturation is a phenomena that occurs when all a circuit's available bandwidth in a given direction is being utilized by a large upload/download."* PingPlotter: tool utama untuk "determine if saturation is being caused by their internet service provider, a wireless network, or bad hardware." Endace: *"saturated bandwidth, high latency or packet loss, that are affecting all traffic."* Min 4 sumber. |
| 2 | **G13** | Kecepatan internet sangat lambat | **0.50** | — | 0.7 → 0.5 (cross-cutting) | User-facing symptom yang juga muncul di P12 (CF 0.5). **Cross-cutting konsisten dengan P12** — di-turun ke 0.5 karena muncul di P09, P10, P11, P12, P08, P02 (banyak problem berbeda). ManageEngine & NetBeez menyebut "slow website loading" di konteks latensi, tapi symptom ini tidak spesifik ke bandwidth. Di P10, G13 adalah user-side mirror dari G22 (objective measurement). Konsistensi dengan P12 (CF 0.5) dijaga. |

### Evidence Summary

- **Signature symptom (objective):** G22 (CF 0.9) — speed test rendah adalah definisi throughput problem.
- **Mirror symptom (subjective):** G13 (CF 0.5) — user-facing "lambat" yang cross-cutting.
- **Rule P10:** 2 gejala — lolos filter "≥ 2 gejala relevan".
- **Konsistensi cross-cutting:** G13 CF 0.5 sama persis dengan P12 (bukan duplikat — sengaja konsisten karena sama-sama cross-cutting kuat).

### Bundling Tutorial Gejala

#### G22 — Speed test hasil sangat rendah

- **short_desc:** Saat menjalankan speed test (speedtest.net, fast.com), hasil download/upload jauh di bawah paket ISP langganan (mis. <30% dari paket 100 Mbps) atau jauh di bawah baseline historical.
- **how_to_check:** `Jalankan speedtest.net atau fast.com. Bandingkan download/upload dengan paket ISP. <30% paket = sangat rendah (indikasi P10). Untuk akurasi: tutup semua background download/stream, connect via Ethernet kalau bisa, test di beberapa waktu berbeda.`

```yaml
tutorial:
  definition: >
    Speed test mengukur throughput aktual (Mbps) antara device dan server
    test. Hasil yang konsisten <30% paket ISP adalah signature bandwidth
    problem. Sonic: "Bandwidth saturation occurs when all available
    bandwidth in a given direction is being utilized." Penting: hasil
    speed test dipengaruhi banyak faktor — WiFi signal, background
    download, ISP peak hours, server test location. Test yang valid harus
    via Ethernet, tanpa background traffic, di jam non-peak. PingPlotter
    menekankan: "determine if saturation is being caused by their internet
    service provider, a wireless network, or bad hardware" — isolasi
    required.
  verification_steps:
    - "Step 1: Tutup semua aplikasi yang konsumsi bandwidth — Steam update, Netflix, download manager, cloud sync (OneDrive, Google Drive)."
    - "Step 2: Connect via Ethernet kabel kalau memungkinkan (WiFi memberi variance besar)."
    - "Step 3: Buka browser, kunjungi speedtest.net (Ookla — standard industri) atau fast.com (Netflix — simpler)."
    - "Step 4: Catat paket ISP Anda (mis. 100 Mbps download, 50 Mbps upload) dari tagihan ISP."
    - "Step 5: Jalankan test. Catat hasil download, upload, dan ping."
    - "Step 6: Ulangi test 3 kali dengan jeda 1 menit. Catat rata-rata."
    - "Step 7: Bandingkan: actual ≥ 80% paket = normal; 50-80% = variance wajar (WiFi/peak hour); <50% = ada masalah; <30% = indikasi kuat P10 (saturation)."
    - "Step 8: Untuk isolasi penyebab — test di jam non-peak (mis. 3AM) vs peak (8PM). Jika peak-hour-only → ISP congestion. Jika konsisten → masalah lokal (lihat common_causes)."
  interpretation: >
    ≥80% paket + ping <50ms: normal | 50-80% paket: variance WiFi atau
    peak-hour wajar | 30-50% paket: ada masalah (latensi, loss, atau
    partial saturation) | <30% paket: indikasi kuat P10 (bandwidth
    saturation atau ISP throttling) | <10% paket: serius, kemungkinan
    hardware issue atau ISP outage partial.
  common_causes:
    - "Bandwidth saturation — banyak user/device share koneksi (Sonic)"
    - "Background download/update (Steam, Windows Update, cloud sync)"
    - "ISP throttling peak hours (terutama ISP consumer-grade)"
    - "QoS misconfiguration di router (Endace, Cisco)"
    - "Malware yang konsumsi bandwidth (botnet, crypto-miner)"
    - "Hardware router tua yang tidak handle speed modern"
    - "WiFi congestion (channel padat di apartment complex)"
  related_symptoms: [G13, G15, G14, G11]
```

#### G13 — Kecepatan internet sangat lambat

> **Cross-reference:** Lihat bundling lengkap di P12 (Gejala cross-cutting). Di P10, G13 adalah user-facing mirror dari G22 (objective speed test) — konsistensi CF_pakar 0.5 dengan P12.

---

