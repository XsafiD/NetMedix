## P11 — Packet Loss Tinggi

**Kategori:** Performa
**Definisi:** Persentase paket data yang gagal mencapai tujuan melebihi threshold >5% — indikator kuat adanya masalah di physical layer (kabel rusak, NIC fault), wireless interference, atau network congestion parah. Berbeda dari P12 (latensi) yang fokus pada waktu RTT, P11 fokus pada paket hilang.
**Sumber utama riset:**

1. Groundcover — "Packet Loss Troubleshooting: Causes, Detection & Prevention" — https://www.groundcover.com/learn/networking/packet-loss-troubleshooting
2. PathSolutions — "Diagnose and Fix Packet Loss in Your Network" — https://www.pathsolutions.com/blog/diagnose-and-fix-packet-loss
3. Check Point Software — "How to Fix Packet Loss in 3 Steps" — https://www.checkpoint.com/cyber-hub/network-security/what-is-packet-loss-and-how-to-prevent-it/how-to-fix-packet-loss-in-3-steps/
4. Fortinet — "What is Packet Loss? How to Fix It?" — https://www.fortinet.com/resources/cyberglossary/what-is-packet-loss
5. PandoraFMS — "Packet Loss in Networks: Diagnosis, Causes and Solutions" — https://pandorafms.com/blog/packet-loss/
6. AVIXA — "How to Fix Packet Loss" — https://www.avixa.org/explore/articles/how-to-fix-packet-loss
7. TSCables — "Troubleshooting Common Ethernet Cable Issues" — https://tscables.com/blogs/news/troubleshooting-common-ethernet-cable-issues

### Tabel CF_pakar

> Rule v1.0.0 sudah berisi 2 gejala (G14, G23) — lolos filter "≥ 2 gejala relevan" tanpa perlu expand. Identitas rule jelas: signature packet loss + dampak intermittent.

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G14** | Ping packet loss > 5% | **0.90** | 0.9 (signature) | — | Signature symptom — definisi packet loss itu sendiri. AVIXA: *"The industry standard threshold for acceptable packet loss is generally less than 1%, with critical applications requiring even tighter."* PathSolutions: *"Packet loss is one of the most common and frustrating network issues, leading to slow connections, poor call quality, and unreliable data transmission."* Groundcover, Check Point, Fortinet, PandoraFMS — semuanya memakai G14 sebagai primary diagnostic indicator. Min 6 sumber independen. |
| 2 | **G23** | Koneksi putus-nyala (intermittent) | **0.60** | 0.5 (supporting) | 0.5 → 0.6 (impact langsung) | Impact langsung dari packet loss parah — user mengalami koneksi putus-nyala karena banyak paket gagal. PandoraFMS: *"Buffering, latency, and slow download speeds are all signs of a problem with the cable."* PathSolutions: packet loss menyebabkan "unreliable data transmission". **Naik** dari 0.5 default karena di P11 G23 adalah *impact langsung* dari G14 (berbeda dari P12 yang menurunkan G23 ke 0.3 karena di P12 G23 cuma edge case cross-cutting). Di P11 G23 lebih dekat ke signature daripada cross-cutting. |

### Evidence Summary

- **Signature symptom:** G14 (CF 0.9) — definisi packet loss itu sendiri.
- **Impact symptom:** G23 (CF 0.6) — konsekuensi langsung packet loss parah.
- **Rule P11:** 2 gejala — lolos filter "≥ 2 gejala relevan".
- **Catatan cross-cutting:** G14 muncul juga di P12 (CF 0.5 — supporting) dan P14 (CF TBD — supporting karena kabel rusak bisa menyebabkan loss). G14 di P11 adalah **signature kuat (0.9)** — nilai CF berbeda per konteks rule sesuai metodologi Opsi D.

### Bundling Tutorial Gejala

> Gejala P11 (G14, G23) sudah di-dokumentasi di P12 (lihat bagian "Bundling Tutorial Gejala P12"). Tidak ada tutorial baru yang perlu ditulis — hanya referensi silang:
>
> - **G14 — Ping packet loss > 5%** → lihat bundling di P12 (signature P11, supporting P12)
> - **G23 — Koneksi putus-nyala / intermittent** → lihat bundling di P12 (cross-cutting)

---

## P13 — Firewall Memblokir Koneksi

**Kategori:** Keamanan
**Definisi:** Aplikasi atau service tertentu tidak bisa berkomunikasi karena diblokir firewall (Windows Defender, third-party, atau hardware firewall di router). Bisa karena rule terlalu ketat, port tertentu ditutup, atau IDS/IPS false positive. Berbeda dari P01 (total connectivity down) — di P13 hanya aplikasi/port tertentu yang terdampak.
**Sumber utama riset:**

1. Microsoft Support — "Firewall and network protection in the Windows Security app" — https://support.microsoft.com/en-us/windows/security/windows-security/firewall-and-network-protection-in-the-windows-security-app
2. ServerFault — "How do you tell WHY Windows Firewall is blocking a program?" — https://serverfault.com/questions/915664/how-do-you-tell-why-windows-firewall-is-blocking-a-program
3. LexisNexis SupportCenter — "How to Add Exceptions to the Windows Firewall" — https://supportcenter.lexisnexis.com/app/answers/answer_view/a_id/1081611/~/how-to-add-exceptions-to-the-windows-firewall-
4. SuperUser — "Firewall allowed app still blocked in Windows 10 x64 Pro" — https://superuser.com/questions/1313309/firewall-allowed-app-still-blocked-in-windows-10-x64-pro
5. Ansys Optics — "Adding inbound rules to Windows defender firewall" — https://optics.ansys.com/hc/en-us/articles/7144748040467-Adding-inbound-rules-to-Windows-defender-firewall
6. Spiceworks Community — "Windows defender firewall 'ON' not allowing application to work" — https://community.spiceworks.com/t/windows-defender-firewall-on-not-allowing-application-to-work/638534

### Tabel CF_pakar

> Rule v1.0.0 berisi G16 + G25. Identitas P13 = selective blocking (aplikasi/port specific) — berbeda dari P01 (semua koneksi down).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G25** | Firewall memblokir aplikasi | **0.90** | 0.9 (signature) | — | Signature symptom — definisi problem itu sendiri. Microsoft Support: *"If the firewall is blocking an app you need, you can add an exception for that app, or open a specific port."* ServerFault: dokumen triase via firewall log + netstat + packet capture. LexisNexis, Ansys, Spiceworks — panduan add exception konsisten. Min 4 sumber. |
| 2 | **G16** | Aplikasi tertentu tidak bisa connect | **0.70** | 0.7 (common) | — | Common symptom dari firewall blocking, tapi tidak definitive — bisa juga disebabkan aplikasi bug, server down (sisi remote), atau routing issue. Spiceworks: user report firewall ON tidak allow aplikasi (TCP Port 3333 blocked). SuperUser: firewall allowed app still blocked — kasus advanced. **Tidak dinaikkan** karena G16 adalah symptom user-facing yang juga bisa muncul di P04 (DNS poisoning → aplikasi tertentu redirect), P03 (DNS gagal resolve server aplikasi), atau aplikasi-side bug. |

### Evidence Summary

- **Signature symptom:** G25 (CF 0.9) — firewall secara eksplisit memblokir aplikasi.
- **User-facing symptom:** G16 (CF 0.7) — aplikasi tertentu tidak connect, perlu diagnosis lanjut.
- **Rule P13:** 2 gejala — lolos filter "≥ 2 gejala relevan".
- **Diferensiasi klinis:** G25 (firewall alert) definitif, G16 (app not connect) perlu verifikasi cause.

### Bundling Tutorial Gejala

#### G16 — Aplikasi tertentu tidak bisa connect

- **short_desc:** Hanya satu atau beberapa aplikasi tertentu (mis. game, email client, file sharing) yang gagal connect, sementara aplikasi lain (browser, chat) normal. Berbeda dari total connectivity down.
- **how_to_check:** `Identifikasi aplikasi yang gagal. Coba aplikasi lain yang mirip (mis. game A gagal, game B normal? Email client gagal tapi webmail normal?). Coba dari jaringan berbeda (hotspot HP) — jika di jaringan lain OK → masalah firewall di jaringan ini.`

```yaml
tutorial:
  definition: >
    "Aplikasi tertentu tidak connect" adalah selective failure — berbeda
    dari P01 (semua aplikasi down). Selective failure menunjukkan
    network-layer OK tapi port/protocol spesifik diblokir. Microsoft
    Support: klasik case firewall rule blocks port 3333, 80, 443. Spiceworks
    thread: user report "TCP Port 3333 is blocked by your firewall". Common
    scenario: game Steam gagal update (port 27036), email Thunderbird gagal
    IMAP (port 993), file sharing SMB gagal (port 445). Bisa juga: aplikasi
    server-side down (bukan problem lokal — test dari jaringan lain untuk
    konfirmasi).
  verification_steps:
    - "Step 1: Identifikasi aplikasi yang gagal connect (mis. Steam, Thunderbird, salah satu game)."
    - "Step 2: Identifikasi port/protocol yang dipakai aplikasi. Cek dokumentasi aplikasi atau `netstat -an | findstr ESTABLISHED` saat aplikasi running."
    - "Step 3: Coba aplikasi lain yang mirip fungsinya (mis. Steam gagal → coba Epic Games atau GOG). Jika aplikasi lain OK → masalah specifik ke app itu (config atau server)."
    - "Step 4: Coba aplikasi yang sama dari device lain di jaringan yang sama. Jika semua device gagal → firewall di router/jaringan. Jika hanya 1 device → firewall lokal (Windows atau third-party)."
    - "Step 5: Test dari jaringan berbeda (hotspot HP). Jika di jaringan lain OK → masalah firewall di jaringan awal."
    - "Step 6: Untuk konfirmasi firewall lokal — disable sementara Windows Defender Firewall (Control Panel → System and Security → Windows Defender Firewall → Turn off). Jika aplikasi jalan → confirmed firewall blocking (segera enable kembali setelah test!)."
    - "Step 7: Cek firewall log: Windows Defender Firewall → Properties → Logging → Customize. Buka log file (.log). Cari entry DROP atau BLOCK untuk port aplikasi."
    - "Step 8: Cek juga antivirus/third-party firewall yang mungkin terinstall (Norton, Kaspersky, Bitdefender) — bisa punya firewall sendiri yang independent."
  interpretation: >
    Hanya 1 aplikasi gagal, semua device: masalah aplikasi-side (server
    down, config salah) | Hanya 1 aplikasi gagal, hanya 1 device: config
    device atau firewall lokal block | Banyak aplikasi dengan port sama
    gagal: firewall blocks port range | Aplikasi gagal hanya di jaringan
    tertentu: firewall jaringan (router/corporate) | Semua aplikasi down:
    bukan G16, lihat P01.
  common_causes:
    - "Windows Defender Firewall blocks port/protocol aplikasi (Microsoft)"
    - "Third-party antivirus firewall (Norton, Kaspersky, Bitdefender)"
    - "Hardware firewall di router/corporate blocks outbound port"
    - "ISP throttling/blocks port tertentu (mis. port 25 SMTP, port 80 personal hosting)"
    - "Application bug atau config salah (bukan network issue)"
    - "Server-side down (test dari jaringan lain untuk konfirmasi)"
    - "IDS/IPS false positive (corporate firewall)"
  related_symptoms: [G25, G39, G31]
```

#### G25 — Firewall memblokir aplikasi

- **short_desc:** Windows atau aplikasi security menampilkan notifikasi/prompt bahwa firewall memblokir aplikasi tertentu, atau firewall log menunjukkan entry DROP/BLOCK untuk port aplikasi. Definitive indicator.
- **how_to_check:** `Cek Windows Defender Firewall → Allow an app through firewall — pastikan aplikasi Anda di-check (terutama kolom Private DAN Public). Cek firewall log (Advanced Settings → Monitoring → Firewall). Cek also aplikasi security pihak ketiga.`

```yaml
tutorial:
  definition: >
    Firewall blocking adalah kondisi definitive di mana sistem keamanan
    (Windows Defender, third-party AV, atau hardware firewall) secara
    eksplisit menolak traffic aplikasi. Berbeda dari G16 (symptom
    user-facing), G25 adalah OS/firewall-level alert atau log entry.
    Microsoft Support: "If the firewall is blocking an app you need, you
    can add an exception for that app, or open a specific port." LexisNexis
    & Ansys: panduan add inbound/outbound rule. ServerFault: triase via
    firewall log, netstat, dan packet capture.
  verification_steps:
    - "Step 1: Buka Windows Security (Win+S → ketik 'Windows Security') → Firewall & network protection."
    - "Step 2: Klik 'Allow an app through firewall'. Scroll daftar — cari aplikasi Anda. Pastikan di-check di kolom Private dan Public."
    - "Step 3: Jika tidak ada di list → klik 'Change settings' → 'Allow another app'. Browse executable aplikasi → Add."
    - "Step 4: Test aplikasi lagi. Jika masih gagal → lanjut ke advanced diagnostics."
    - "Step 5: Buka Windows Defender Firewall → Advanced settings → Inbound Rules. Cari rule dengan Action=Block yang match aplikasi Anda (atau port yang dipakai)."
    - "Step 6: Cek Outbound Rules juga. Beberapa AV firewall ketat untuk outbound."
    - "Step 7: Buka Windows Defender Firewall → Properties → tab untuk profile (Domain/Private/Public) → Logging → Customize. Note path log file (default: %SystemRoot%\\System32\\LogFiles\\Firewall\\pfirewall.log)."
    - "Step 8: Buka log file tsb. Cari entry 'DROP' atau 'BLOCK' untuk port aplikasi Anda. Timestamp akan match saat aplikasi gagal connect."
    - "Step 9: Jika ada AV third-party (Norton, Kaspersky, dll) — buka AV console → Firewall settings → cek aplikasi rule list."
  interpretation: >
    Aplikasi tidak ada di allow list: belum di-allow → add exception |
    Aplikasi ada di allow list tapi masih gagal: kemungkinan inbound rule
    blocks port → cek Inbound Rules | Log firewall menunjukkan DROP untuk
    port aplikasi: confirmed firewall blocking (G25) | Tidak ada entry log:
    bukan firewall, mungkin aplikasi-side atau server-side issue | AV
    third-party dengan firewall sendiri: cek konsol AV.
  common_causes:
    - "Aplikasi belum di-allowlist di Windows Firewall (Microsoft)"
    - "Inbound rule blocks port spesifik (mis. game port 27036, RDP 3389)"
    - "Outbound rule terlalu ketat (third-party AV)"
    - "Hardware firewall di router blocks port (ISP atau corporate)"
    - "Profile salah — app di-allow di Private tapi connect dari Public network"
    - "Firewall rule corrupt setelah Windows Update"
    - "Group Policy corporate yang enforce strict firewall"
  related_symptoms: [G16, G39, G31]
```

---

## P14 — Kerusakan Kabel / Konektor Jaringan

**Kategori:** Hardware
**Definisi:** Kabel UTP/patch cord putus, konektor RJ45 longgar atau rusak, atau crimping buruk — menyebabkan physical layer (Layer 1) bermasalah. Berbeda dari P15 (hardware device rusak) — di P14 problem ada di kabel/konektor di antara device. Tanda khas: link lamp NIC/switch mati/berkedip, atau packet loss tinggi akibat kabel partial damage.
**Sumber utama riset:**

1. TSCables — "Troubleshooting Common Ethernet Cable Issues" — https://tscables.com/blogs/news/troubleshooting-common-ethernet-cable-issues
2. Noyafa — "How to Detect a Broken Ethernet Cable: Signs and Fixes" — https://www.noyafa.com/blogs/knowledge-base/detect-broken-ethernet-cable
3. Zion Communication — "Why Bad Ethernet Connectors Kill Your Network Speed (And How to Fix It)" — https://www.zion-communication.com/Why-Bad-Ethernet-Connectors-Kill-Your-Network-Speed-And-How-to-Fix-It-id46456296.html
4. CoaxialCableCN — "Bad Ethernet Cable Symptoms" — https://www.coaxialcablecn.com/info/bad-ethernet-cable-symptoms-99017545.html
5. SuperUser — "Can a wrongly crimped Ethernet Cable work, but not as intended?" — https://superuser.com/questions/1240352/can-a-wrongly-cimped-ethernet-cable-work-but-not-as-intended
6. Quora — "Can a bad Ethernet cable cause packet loss?" — https://www.quora.com/Can-a-bad-Ethernet-cable-cause-packet-loss

### Tabel CF_pakar

> Rule v1.0.0 berisi G18 + G29 + G14. Identitas P14 = physical layer (kabel/konektor) damage — berbeda dari P15 (device hardware failure).

| No | Kode | Nama Gejala | CF_pakar | Skala Default | Override | Justifikasi / Sumber |
|---|---|---|---|---|---|---|
| 1 | **G29** | Kabel terlihat rusak / longgar | **0.95** | 0.9 (signature) | 0.9 → 0.95 (definitive physical inspection) | Definitif via inspeksi visual — kabel terkelupas, bengkok berlebihan, atau konektor RJ45 retak/longgar. TSCables: *"Damaged cables and faulty connectors are common causes of packet loss."* Noyafa: *"Physical damage: Bending, pinching, or crushing the cable. Wear and tear: Frequent plugging and unplugging."* CoaxialCableCN: bad ethernet cable symptoms. **Naik** ke 0.95 karena definitive — physical evidence yang tidak perlu tool diagnostic. Hampir tidak ada false positive (asalkan inspeksi benar). |
| 2 | **G18** | Link lamp NIC/switch mati/berkedip | **0.90** | 0.9 (signature) | — | Signature diagnostic indicator — lampu link di NIC atau switch port menyala/berkedip abnormal (mati saat kabel terpasang, atau berkedip merah/oranye cepat). Zion Communication: connector quality impact ke link indicator. Berbeda dari G33 (lampu LAN di router mati → P15 hardware router port), G18 adalah di NIC device atau di switch port (device-side atau middle-of-link). Min 4 sumber konsisten. |
| 3 | **G14** | Ping packet loss > 5% | **0.70** | 0.5 (supporting) | 0.5 → 0.7 (impact langsung dari partial kabel damage) | Impact langsung dari kabel partial damage — kabel tidak putus total (masih ada link) tapi paket banyak yang corrupt/drop karena crosstalk atau pin rusak. TSCables: *"Damaged cables and faulty connectors are common causes of packet loss."* Quora: jawaban pakar menyebut kabel bad menyebabkan packet loss intermittent. **Naik** dari 0.5 default (cross-cutting) karena di P14 G14 adalah impact langsung mekanisme fisik (partial kabel damage). Konsistensi dengan P11 (signature 0.9) dan P12 (supporting 0.5) — di P14 G14 menempati posisi tengah (impact langsung dari mekanisme spesifik). |

### Evidence Summary

- **Definitive physical signature:** G29 (CF 0.95) — visual inspection.
- **Diagnostic signature:** G18 (CF 0.9) — link lamp abnormal.
- **Performance impact:** G14 (CF 0.7) — packet loss dari partial damage.
- **Rule P14:** 3 gejala — lolos filter "≥ 2 gejala relevan" dengan kombinasi kaya.
- **Diferensiasi klinis:** G33 (lampu LAN router mati → P15 router) vs G18 (lampu link di NIC/switch → P14 kabel/device port).

### Bundling Tutorial Gejala

#### G18 — Link lamp NIC/switch mati/berkedip

- **short_desc:** Lampu indikator link di port NIC device atau di switch port mati (saat kabel terpasang dan device aktif) atau berkedip abnormal (merah cepat, atau off-on-off terus menerus). Indikator Layer 1 (physical) problem.
- **how_to_check:** `Lihat fisik port Ethernet di laptop/PC (NIC) dan di switch/router (port). Saat kabel terpasang dan kedua device ON, lampu harus menyala hijau/oranye stabil + berkedip saat ada traffic. Jika mati atau berkedip abnormal → G18.`

```yaml
tutorial:
  definition: >
    Lampu link di NIC dan switch port adalah indicator Layer 1 (physical
    layer). Zion Communication: connector quality langsung impact ke link
    establishment. Dua lampu typical: LINK (menyala saat link establish)
    dan ACT (activity, berkedip saat ada traffic). Behavior abnormal:
    mati total padahal kabel terpasang, atau berkedip cepat (sign of
    intermittent link — kabel partial damage). Berbeda dari G33 (lampu
    LAN di router mati → P15 router port rusak), G18 adalah di NIC device
    atau switch port yang menghubungkan ke kabel tsb.
  verification_steps:
    - "Step 1: Identifikasi port Ethernet di device Anda (NIC di laptop/PC) dan di switch/router."
    - "Step 2: Pastikan kabel terpasang dengan klik di kedua ujung. Cabut dan pasang lagi untuk memastikan."
    - "Step 3: Lihat lampu di NIC device Anda (biasanya dekat port Ethernet). Saat kabel terpasang dan device ON, lampu harus menyala stabil (hijau/oranye) + berkedip saat ada data."
    - "Step 4: Lihat lampu di switch/router port yang sama (port tempat kabel Anda connect). Lampu juga harus menyala stabil."
    - "Step 5: Jika lampu MATI TOTAL padahal kabel terpasang di kedua ujung dan kedua device ON → G18 confirmed → kemungkinan kabel putus atau port rusak."
    - "Step 6: Jika lampu BERKEDIP CEPAT (off-on-off terus menerus) → indikasi intermittent link — kabel partial damage atau konektor longgar."
    - "Step 7: Jika lampu menyala saat kabel di-gerak-gerak → konektor RJ45 longgar atau pin bengkok — kabel perlu re-crimp atau ganti."
    - "Step 8: Swap dengan kabel yang diketahui working. Jika kabel baru link OK → confirmed kabel original rusak (lihat G29)."
    - "Step 9: Jika kabel baru juga G18 → port NIC atau switch port yang rusak (lihat P15 atau P01)."
  interpretation: >
    Lampu mati padahal kabel terpasang + device ON: kabel putus atau port
    rusak | Lampu berkedip cepat: intermittent link, kabel partial damage
    | Lampu menyala saat digerakkan: konektor longgar, re-crimp atau
    ganti kabel | Kabel baru solve problem: confirmed kabel original rusak
    | Kabel baru juga bermasalah: port NIC atau switch port rusak.
  common_causes:
    - "Kabel UTP putus di tengah (TSCables)"
    - "Konektor RJ45 longgar — pin tidak kontak penuh (Zion Communication)"
    - "Pin RJ45 bengkok atau patah"
    - "Crimping buruk — wire tidak ter-Punch ke jalur yang benar (SuperUser)"
    - "Port NIC device rusak (pin port bengkok atau korosi)"
    - "Switch port rusak (lihat P15)"
    - "Kabel terlalu panjang (>100m untuk Ethernet standard) atau terlalu pendek dengan bending tidak wajar"
  related_symptoms: [G29, G14, G33, G20]
```

#### G29 — Kabel terlihat rusak / longgar

- **short_desc:** Inspeksi visual kabel menemukan kerusakan fisik: kabel terkelupas, bengkok berlebihan, terpotong, tergigit hewan, atau konektor RJ45 retak/patah/pin bengkok. Definitif physical evidence.
- **how_to_check:** `Inspeksi visual sepanjang kabel — dari device sampai switch/router. Cari: kabel terkelupas, bengkok tajam, retak, bekas gigitan/tindihan. Cek konektor RJ45 di kedua ujung: pin lurus semua, plastik lock tidak patah, body tidak retak. Jika ada kerusakan → G29.`

```yaml
tutorial:
  definition: >
    Inspeksi visual adalah cara definitif dan tercepat untuk deteksi
    kerusakan kabel. TSCables: "Damaged cables and faulty connectors are
    common causes of packet loss." Noyafa: "Physical damage: Bending,
    pinching, or crushing the cable · Wear and tear: Frequent plugging
    and unplugging · Environmental factors: Heat." CoaxialCableCN:
    bad ethernet cable symptoms. Tipe kerusakan umum: 1) Outer jacket
    terkelupas (exposed twisted pair); 2) Bending tidak wajar ( Ethernet
    min bend radius = 4x diameter); 3) RJ45 retak atau pin bengkok;
    4) Crimping salah (wire tidak masuk jalur atau warna urutan salah
    T568A/T568B).
  verification_steps:
    - "Step 1: Cabut kabel dari kedua ujung (device dan switch/router)."
    - "Step 2: Inspeksi sepanjang kabel — pegang dan gerakkan tangan dari ujung ke ujung. Cari: kabel terkelupas, bengkok tajam, retak di outer jacket, tanda gigitan hewan, tanda terbakar/melting."
    - "Step 3: Cek konektor RJ45 di kedua ujung: pin emas harus lurus semua (tidak bengkok/patah), plastik lock (clip) tidak patah, body plastik tidak retak."
    - "Step 4: Untuk konfirmasi urutan crimping — lihat pin dari bawah (clip menghadap bawah). Standar T568B (paling umum): pin 1-8 warna orange-stripes/orange/green-stripes/blue/blue-stripes/green/brown-stripes/brown. Standar T568A: swap orange↔green. Kabel straight-through harus sama di kedua ujung (T568B-T568B)."
    - "Step 5: Test dengan cable tester (alat khusus). Pasang remote dan main di kedua ujung, tekan tombol. Lampu 1-8 harus menyala berurutan di kedua sisi. Jika ada pin yang tidak menyala → wire itu putus atau tidak ter-crimp."
    - "Step 6: Jika tidak ada cable tester — pakai multimeter: set ke continuity/beep mode, test pasangan pin (ujung A pin 1 ke ujung B pin 1, dst). Harus beep semua 8 pin."
    - "Step 7: Jika kerusakan ditemukan (terkelupas, pin bengkok, urutan salah, atau tester menunjukkan pin putus) → G29 confirmed."
    - "Step 8: Fix: ganti kabel baru (paling cepat dan murah), atau re-crimp konektor RJ45 kalau hanya ujung yang rusak dan kabel masih cukup panjang."
  interpretation: >
    Tidak ada kerusakan visual + tester OK: kabel baik → lihat G18 atau
    G14 untuk symptom lain | Kerusakan visual minor (terkelupas tipis di
    outer jacket, twisted pair masih utuh): mungkin masih working tapi
    rentan fail di masa depan | Konektor RJ45 pin bengkok/patah: confirmed
    G29, re-crimp atau ganti | Urutan crimp salah: confirmed G29, re-crimp
    dengan urutan benar | Cable tester menunjukkan pin putus: confirmed
    G29, ganti kabel.
  common_causes:
    - "Outer jacket terkelupas akibat gesekan dengan tepi tajam (TSCables)"
    - "Bending tidak wajar — kabel tertekuk tajam di sudut (melewati minimum bend radius)"
    - "Tergigit hewan (tikus, kucing) atau tertindih furniture berat"
    - "Wear and tear — sering cabut-pasang dengan tarikan (Noyafa)"
    - "Environmental — panas berlebih di attic, eksposur UV, kelembaban korosi pin"
    - "Crimping buruk dari pabrik atau homemade (SuperUser thread)"
    - "Pin RJ45 patah akibat jatuh atau tersangkut"
  related_symptoms: [G18, G14, G33, G20]
```

#### G14 — Ping packet loss > 5%

> **Cross-reference:** Lihat bundling lengkap di P12 (Packet Loss cross-cutting). Di P14, G14 adalah **impact langsung dari partial kabel damage** (CF 0.7). Mekanisme: kabel tidak putus total (masih ada link, lampu menyala) tapi pin/konektor bermasalah → paket banyak yang corrupt/drop. Konsistensi: G14 di P11 (signature 0.9), P14 (impact langsung 0.7), P12 (cross-cutting supporting 0.5) — sesuai metodologi Opsi D (nilai berbeda per konteks rule).

---

## Orphan Permanen Tutorial Stubs — G31, G32 (VPN Out-of-Scope)

> **Fase 1.E — bundling tutorial stubs untuk 2 orphan permanen.** Sesuai PRD v2.0.0 Non-Goal #1 ("Menambah problem baru di luar 15 existing"), VPN troubleshooting tetap di luar scope diagnosis engine. Namun untuk konsistensi UX di route `/tutorial/<code>`, ke dua gejala ini tetap diberikan stub tutorial yang menjelaskan status out-of-scope dan menunjukkan ke sumber eksternal. Stub tidak dipakai oleh rule manapun (tidak ada `cf_pakar`) — hanya untuk completeness konten `symptoms.json` agar halaman tutorial tidak 404 saat diakses langsung. UI `symptoms.html` akan menampilkan kedua gejala ini sebagai checkbox **disabled** dengan badge "belum didukung sistem" (lihat badge plan di section "Fase 1.C — Decision 5").

### G31 — VPN tidak bisa connect

- **short_desc:** VPN client gagal membuat koneksi ke VPN server. Symptom umum: "VPN connection failed", "authentication failed", "VPN has stopped working", atau handshake timeout berkepanjangan. Berbeda dari G02 (internet putus total) — di G31 internet regular biasanya masih berfungsi, hanya tunnel VPN yang gagal establish.
- **how_to_check:** `Coba connect via VPN client (OpenVPN, WireGuard, Cisco AnyConnect, FortiClient, atau client corporate). Amati error: "authentication failed" → credential/MFA issue; "connection timeout" → network blok port VPN; "certificate validation failed" → cert expired/revoked; "no route to host" → server VPN unreachable.`

```yaml
tutorial:
  definition: >
    Gejala "VPN tidak bisa connect" berada di luar scope diagnosis NetMedix
    v2.0.0 (PRD Non-Goal #1: "Menambah problem baru di luar 15 existing").
    VPN troubleshooting adalah domain spesifik yang berbeda dari network
    troubleshooting umum — failure mode VPN melibatkan authentication
    (password, MFA, RADIUS), certificate (PKI, expired, revoked), protocol
    (OpenVPN, WireGuard, IKEv2, L2TP/IPSec, SSTP), NAT-T compatibility,
    firewall rules spesifik per protocol, dan server-side availability.
    ITU Online: "When a VPN fails, the problem is rarely 'the VPN' by
    itself. It could be an authentication issue, a blocked protocol, bad
    DNS, a local firewall rule, or a provider outage." Gejala ini
    ditandai sebagai "belum didukung sistem" di UI — user yang mengalaminya
    diarahkan ke IT helpdesk corporate atau dokumentasi vendor VPN.
  verification_steps:
    - "Step 1: Identifikasi VPN client yang dipakai (corporate: Cisco AnyConnect, FortiClient, GlobalProtect; personal: NordVPN, ExpressVPN, WireGuard, OpenVPN)."
    - "Step 2: Catat pesan error eksak saat connect gagal (screenshot jika perlu) — pesan ini kunci diagnosa VPN."
    - "Step 3: Verifikasi koneksi internet regular masih jalan (buka website, ping 8.8.8.8). Jika internet juga down → masalah P02, bukan VPN."
    - "Step 4: Coba VPN dari jaringan berbeda (hotspot HP). Jika berhasil → jaringan awal memblok port VPN (corporate firewall, ISP filter, atau hotspot cellular restrict)."
    - "Step 5: Cek credential VPN — username, password, MFA token. Hubungi admin corporate untuk konfirmasi account aktif."
    - "Step 6: Untuk VPN corporate — hubungi IT helpdesk. Mereka punya akses ke VPN server log dan bisa troubleshoot server-side (cert, RADIUS, concurrent session limit)."
    - "Step 7: Konsultasi dokumentasi resmi vendor VPN (Cisco, Palo Alto GlobalProtect, OpenVPN) atau community forum (Reddit r/VPN, vendor support)."
  interpretation: >
    Internet OK + VPN gagal: confirmed VPN-side issue (out-of-scope
    NetMedix) | Internet juga gagal: bukan VPN, lihat P02 (WAN down) |
    VPN gagal di satu jaringan saja: jaringan blok port VPN → hubungi
    admin jaringan | "Authentication failed": credential/cert/MFA issue,
    hubungi admin corporate | "Connection timeout": port VPN diblokir
    (UDP 1194 OpenVPN, TCP 443 AnyConnect, UDP 500/4500 IKEv2) | VPN
    pernah jalan lalu gagal: cert expired atau server maintenance —
    hubungi vendor/admin.
  common_causes:
    - "Credential VPN salah atau expired (password, MFA token expired)"
    - "Client certificate expired atau revoked (PKI corporate)"
    - "Port VPN diblokir firewall (UDP 1194, TCP 443, UDP 500/4500)"
    - "VPN server down atau maintenance (cek status page vendor)"
    - "NAT-T incompatibility (L2TP/IPSec di belakang NAT aggressive)"
    - "Concurrent session limit tercapai (license VPN corporate penuh)"
    - "Client VPN outdated — perlu update ke versi server-compatible"
    - "Split-tunnel atau route conflict setelah VPN establish sebagian"
  related_symptoms: [G02, G03, G16, G39]
```

### G32 — VPN internal gagal (tunnel up, resource internal tidak reachable)

- **short_desc:** Status VPN client menunjukkan "Connected" / "Tunnel established", tetapi resource internal (file server, intranet, internal apps, shared printer) tidak bisa diakses. Berbeda dari G31 (VPN tidak bisa connect sama sekali) — di G32 tunnel berhasil establish tetapi routing/DNS internal bermasalah.
- **how_to_check:** `Setelah VPN status "Connected", test: ping IP server internal (mis. ping 10.0.0.X), akses UNC path (\\fileserver\share), buka intranet URL (http://intranet.corp.local). Jika semua gagal → G32. Cek juga: ipconfig (apakah ada adapter VPN baru?), route print (apakah ada route ke subnet internal?), nslookup internal hostname (apakah DNS VPN push berfungsi?).`

```yaml
tutorial:
  definition: >
    Gejala "VPN connected tapi no internal access" juga berada di luar
    scope diagnosis NetMedix v2.0.0 (PRD Non-Goal #1). VPN post-connection
    troubleshooting melibatkan: split-tunnel vs full-tunnel config, DNS
    push dari VPN server (DNS internal vs DNS public), route injection
    (static route ke subnet internal), firewall rules di sisi VPN gateway,
    dan application-layer authentication internal (SSO, Kerberos). IT
    Support Group: "'VPN is down' might mean the whole company cannot
    connect, one user forgot their password, someone's home Wi-Fi is
    falling over, MFA is not sending, DNS is broken after connection, or
    the user is trying to connect from a hotel network that hates joy."
    Stub ini menjelaskan scope dan mengarahkan user ke IT helpdesk atau
    dokumentasi vendor VPN.
  verification_steps:
    - "Step 1: Konfirmasi VPN status benar-benar 'Connected' — cek icon VPN client, atau `ipconfig` (harus ada adapter VPN baru, mis. 'PPP adapter VPN')."
    - "Step 2: Catat IP VPN yang didapat (mis. 10.0.50.X) dan subnet internal target (mis. 10.0.0.0/24)."
    - "Step 3: Test ping IP server internal berdasar IP, bukan hostname: `ping 10.0.0.5`. Jika ping OK tapi hostname gagal → DNS push issue. Jika ping juga RTO → routing issue."
    - "Step 4: Cek routing table: `route print`. Cari entry ke subnet internal (mis. 10.0.0.0 mask 255.255.255.0 → gateway VPN). Jika tidak ada → split-tunnel config salah."
    - "Step 5: Test DNS internal: `nslookup intranet.corp.local`. Jika 'server unknown' atau resolve ke IP public → DNS VPN tidak push atau leak DNS public."
    - "Step 6: Untuk VPN corporate — hubungi IT helpdesk dengan detail: IP VPN, subnet target, hasil ping, dan nslookup. Mereka bisa cek VPN gateway log dan policy."
    - "Step 7: Cek dokumentasi vendor: Cisco AnyConnect / Palo Alto GlobalProtect / OpenVPN Access Server punya troubleshooting guide spesifik untuk split-tunnel dan DNS push."
  interpretation: >
    VPN Connected + ping IP internal OK + hostname gagal: DNS push issue
    (DNS VPN tidak dikonfigurasi) | VPN Connected + ping IP internal RTO:
    routing/split-tunnel issue (route ke subnet internal tidak di-inject)
    | VPN Connected + sebagian resource OK sebagian gagal: ACL firewall
    VPN gateway membatasi akses per-subnet | VPN Connected + aplikasi
    internal minta login ulang terus: SSO/Kerberos ticket tidak forward
    via VPN | VPN Connected + UNC path lambat: MTU mismatch (VPN
    overhead mengurangi MTU).
  common_causes:
    - "Split-tunnel config salah — hanya traffic internet yang lewat VPN, traffic internal tetap via route lokal"
    - "DNS internal tidak di-push oleh VPN server (DNS leak ke resolver public)"
    - "Route static ke subnet internal tidak di-inject (routing table kosong)"
    - "ACL firewall VPN gateway membatasi akses ke subnet tertentu saja"
    - "MTU mismatch — VPN overhead (encapsulation) menyebabkan fragmentation parah"
    - "SSO/Kerberos ticket tidak forward melalui VPN tunnel"
    - "VPN gateway policy restrict akses berdasar group/role user"
    - "Subnet internal conflict dengan subnet lokal user (mis. keduanya 192.168.1.0/24)"
  related_symptoms: [G31, G03, G04, G07]
```

---

