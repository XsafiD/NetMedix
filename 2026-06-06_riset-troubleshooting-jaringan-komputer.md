---
created_at: 2026-06-06
topic: "Riset Mendalam: Sistem Pakar Troubleshooting Jaringan Komputer"
tags: [sistem-pakar, expert-system, troubleshooting, jaringan-komputer, network, forward-chaining, certainty-factor, uas]
source_urls:
  - "https://jiki.jurnal-id.com/index.php/jiki/article/download/17/13"
  - "https://jurnal.sttmcileungsi.ac.id/index.php/infotech/article/download/397/415/"
  - "https://prosiding.unipma.ac.id/index.php/SENATIK/article/view/2899"
  - "https://obkio.com/blog/common-network-problems/"
  - "https://www.ninjaone.com/blog/common-network-issues/"
  - "https://www.pynetlabs.com/network-issues-and-their-solutions/"
  - "https://networkcheckr.com/how-to-troubleshoot-network-connectivity/"
suggested_location: "03_RISET"
status: inbox
ai_model: "Claude 4.7 Sonnet"
related_files:
  - "[Perbandingan Sistem Pakar UAS](2026-06-05_perbandingan-sistem-pakar-uas.md)"
  - "[Sistem Pakar: Konsep & Arsitektur](2026-04-09_sistem-pakar-expert-system.md)"
  - "[Project Ideas Sistem Pakar](2026-04-09_project-ideas-sistem-pakar.md)"
  - "[Certainty Factor](2026-04-23_certainty-factor.md)"
  - "[Dempster-Shafer Theory](2026-04-23_dempster-shafer-theory.md)"
  - "[Negnevitsky - Expert Systems](../03_RISET/2026-03-13_artificial-intelligence-negnevitsky.md)"
---

# Riset Mendalam: Sistem Pakar Troubleshooting Jaringan Komputer

## Executive Summary

Dokumen ini merupakan hasil riset mendalam untuk membangun **sistem pakar troubleshooting jaringan komputer** sebagai tugas UAS Sistem Cerdas. Domain ini dipilih berdasarkan rekomendasi dari [dokumen perbandingan](2026-06-05_perbandingan-sistem-pakar-uas.md) yang menempatkannya di posisi TOP 3 (Score 26).

**Keputusan utama:**
- **Metode Inferensi:** Forward Chaining + Certainty Factor (kombinasi)
- **Sumber Pengetahuan:** Studi literatur internet (dokumentasi teknis, jurnal, forum) - tanpa wawancara langsung ke pakar
- **Jumlah Masalah:** 15 masalah jaringan utama yang akan didiagnosis
- **Jumlah Gejala:** 40-50 gejala untuk diagnosis

---

## Related Discussions

- **Previous Discussion:** [Perbandingan Sistem Pakar untuk UAS](2026-06-05_perbandingan-sistem-pakar-uas.md) (2026-06-05)
- **Project Ideas:** [Project Ideas: Sistem Pakar](2026-04-09_project-ideas-sistem-pakar.md) (2026-04-09)
- **Metode:** [Certainty Factor](2026-04-23_certainty-factor.md), [Dempster-Shafer](2026-04-23_dempster-shafer-theory.md)

---

## 1. Latar Belakang Domain

### 1.1 Mengapa Troubleshooting Jaringan?

Jaringan komputer adalah infrastruktur kritis di era digital. Masalah jaringan bisa menyebabkan downtime, kerugian produktivitas, dan frustrasi pengguna. Namun, tidak semua pengguna memiliki keahlian untuk mendiagnosis masalah jaringan. Sistem pakar dapat membantu:

- **Pengguna awam** mendapatkan diagnosis awal sebelum memanggil teknisi
- **Teknisi junior** mempercepat proses troubleshooting
- **Administrator jaringan** memiliki asisten diagnosis 24/7

### 1.2 Keunggulan Domain untuk UAS

| Faktor | Penilaian | Alasan |
|--------|-----------|--------|
| Ketersediaan Sumber | Sangat Baik | Dokumentasi teknis, RFC, vendor guide, forum |
| Kemudahan Implementasi | Baik | Aturan IF-THEN jelas, gejala terdefinisi |
| Referensi Indonesia | Ada | Beberapa jurnal lokal membahas topik ini |
| Relevansi | Tinggi | Mahasiswa Informatika familiar dengan jaringan |
| Daya Tarik Presentasi | Tinggi | Demo live, contoh kasus nyata |

---

## 2. Sumber Pengetahuan

### 2.1 Sumber Utama (Tanpa Wawancara Pakar)

Semua pengetahuan diperoleh dari sumber terbuka di internet:

#### A. Dokumentasi Teknis Resmi

| Sumber | URL | Coverage |
|--------|-----|----------|
| Cisco Networking Docs | cisco.com/c/en/us/support/ | Routing, switching, wireless enterprise |
| Microsoft Network Troubleshooting | learn.microsoft.com | Windows networking, DNS, DHCP |
| CompTIA Network+ Guide | comptia.org | Best practice troubleshooting |
| IEEE Standards | standards.ieee.org | Standar jaringan (802.11, 802.3) |
| IETF RFC Documents | rfc-editor.org | Standar protokol (DNS, DHCP, TCP/IP) |

#### B. Panduan Troubleshooting Umum

| Sumber | Coverage |
|--------|----------|
| Obkio - Common Network Problems | 16 masalah jaringan umum + solusi |
| NinjaOne - Common Network Issues | 8 masalah + cara fix |
| PyNet Labs - Network Issues | 10 masalah + solusi |
| NetworkCheckr - 7-Step Guide | Panduan troubleshooting sistematis |
| Auvik - Network Diagnostics | Wireless diagnosis guide |

#### C. Jurnal Indonesia (Referensi Implementasi)

| No | Judul | Penulis/Tahun | Metode | Key Insight |
|----|-------|---------------|--------|-------------|
| 1 | Sistem Pakar Troubleshooting Jaringan LAN | Nurmanta & Fachrie (2020) | FC + CF | Forward Chaining + Certainty Factor untuk gangguan LAN |
| 2 | Sistem Pakar Deteksi Kerusakan Jaringan Internet Indihome | Sya'i et al. (2022) - JIKI | FC | 15 gangguan, 6 solusi, berbasis web PHP+MySQL |
| 3 | Aplikasi Sistem Pakar Diagnosa Troubleshooting Jaringan LAN | STTM Cileungsi (2023) | Backward Chaining | Perbandingan metode inferensi |
| 4 | Sistem Pakar Diagnosa Kegagalan Koneksi TCP/IP | SENATIK UNIPMA | FC | Fokus TCP/IP stack failure |
| 5 | Sistem Pakar Troubleshooting Jaringan Komputer | Asnawi & Sunarto (2021) - Device | CF | Certainty Factor, akurasi tinggi |

#### D. Forum & Komunitas

- **Stack Overflow / Network Engineering** - Q&A troubleshooting spesifik
- **Reddit r/networking** - Diskusi kasus nyata
- **Cisco Learning Network** - Lab scenario dan troubleshooting
- **Kaskus / Forum Indonesia** - Kasus lokal (Indihome, WiFi rumah, LAN kantor)

### 2.2 Validasi Pengetahuan

Karena tidak ada wawancara langsung dengan pakar, validasi dilakukan melalui:

1. **Cross-referencing** antar sumber (minimal 2 sumber independent per aturan)
2. **Konsistensi** dengan standar industri (Cisco, CompTIA, Microsoft)
3. **Common practice** yang disepakati di komunitas teknis
4. **Testing** terhadap skenario yang sudah diketahui hasilnya

---

## 3. Daftar Masalah Jaringan yang Akan Didiagnosis

Berikut adalah **15 masalah jaringan** ("penyakit") yang akan didiagnosis oleh sistem pakar kita:

### 3.1 Kategori: Konektivitas Dasar

#### P01 - Tidak Ada Koneksi Jaringan (No Network Connectivity)
- **Deskripsi:** Perangkat tidak terhubung ke jaringan sama sekali, tidak bisa mengakses lokal maupun internet
- **Penyebab Umum:** NIC disabled, kabel putus, switch port mati, driver NIC bermasalah
- **Gejala:** Tidak ada IP address, media disconnected, lampu NIC tidak menyala
- **Solusi:** Cek NIC, ganti kabel, cek switch port, update driver

#### P02 - Koneksi Internet Terputus (No Internet Access)
- **Deskripsi:** Jaringan lokal berfungsi, tetapi tidak bisa akses internet
- **Penyebab Umum:** Gateway tidak terjangkau, ISP down, NAT misconfiguration
- **Gejala:** Bisa ping gateway, tidak bisa ping 8.8.8.8, lampu WAN router merah
- **Solusi:** Restart router, cek kabel WAN, hubungi ISP

### 3.2 Kategori: DNS

#### P03 - DNS Resolution Failure (Gagal Resolusi Nama Domain)
- **Deskripsi:** Bisa ping IP publik, tapi tidak bisa mengakses website via domain
- **Penyebab Umum:** DNS server tidak terkonfigurasi, DNS server down, DNS cache corrupt
- **Gejala:** `ping 8.8.8.8` berhasil, `ping google.com` gagal, `nslookup` gagal
- **Solusi:** Ganti DNS (8.8.8.8 / 1.1.1.1), flush DNS cache, cek DNS setting

#### P04 - DNS Cache Poisoning / Hijacking
- **Deskripsi:** Domain di-resolve ke IP yang salah, redirect ke situs tidak dikenal
- **Penyebab Umum:** Malware, DNS cache corrupt, DNS server dikompromi
- **Gejala:** Website yang biasa diakses mengarah ke halaman aneh, hasil nslookup berbeda antar device
- **Solusi:** Flush DNS, scan malware, gunakan DNS terpercaya

### 3.3 Kategori: DHCP & IP Configuration

#### P05 - DHCP Failure (Gagal Mendapatkan IP dari DHCP)
- **Deskripsi:** Perangkat mendapat IP APIPA (169.254.x.x) atau tidak mendapat IP sama sekali
- **Penyebab Umum:** DHCP server down, DHCP scope habis, port UDP 67/68 diblokir
- **Gejala:** IP address 169.254.x.x, status "Unidentified network", tidak bisa komunikasi
- **Solusi:** Restart DHCP service, perluas scope, cek ACL

#### P06 - IP Address Conflict (Konflik IP)
- **Deskripsi:** Dua atau lebih perangkat menggunakan IP address yang sama
- **Penyebab Umum:** Static IP bentrok dengan DHCP pool, salah konfigurasi manual
- **Gejala:** Pop-up "IP address conflict", koneksi putus-nyala, ping ke IP sendiri ada reply
- **Solusi:** Release/renew IP, ubah static IP, perkecil DHCP pool

#### P07 - Subnet Mask / Default Gateway Salah
- **Deskripsi:** Konfigurasi IP salah sehingga tidak bisa komunikasi ke jaringan luar
- **Penyebab Umum:** Manual misconfiguration, DHCP memberikan setting salah
- **Gejala:** Bisa ping lokal tapi tidak ke luar subnet, subnet mask berbeda dari device lain
- **Solusi:** Koreksi subnet mask, set gateway yang benar, switch ke DHCP

### 3.4 Kategori: Wireless / WiFi

#### P08 - Tidak Bisa Connect ke WiFi
- **Deskripsi:** Perangkat tidak bisa terhubung ke jaringan WiFi
- **Penyebab Umum:** Password salah, SSID hidden, security mode tidak kompatibel, driver WiFi outdated
- **Gejala:** "Cannot connect to network", gagal autentikasi, SSID tidak muncul
- **Solusi:** Forget network & reconnect, update driver, cek security mode (WPA2/WPA3)

#### P09 - WiFi Signal Lemah / Interferensi
- **Deskripsi:** WiFi connect tapi speed rendah, sering disconnect
- **Penyebab Umum:** Jarak terlalu jauh, dinding/halangan, interferensi channel, terlalu banyak client
- **Gejala:** Signal bar hanya 1-2, speed test rendah, sering putus
- **Solusi:** Pindah channel (2.4GHz/5GHz), dekatkan ke AP, gunakan repeater

### 3.5 Kategori: Performa Jaringan

#### P10 - Jaringan Lambat (Slow Network / Bandwidth Saturation)
- **Deskripsi:** Koneksi ada tapi kecepatan sangat rendah
- **Penyebab Umum:** Bandwidth penuh, QoS tidak ada, background download, malware
- **Gejala:** Speed test jauh di bawah paket, loading lama, timeout
- **Solusi:** Monitor bandwidth usage, set QoS, cek background app, scan malware

#### P11 - Packet Loss Tinggi
- **Deskripsi:** Paket data hilang saat transmisi, menyebabkan komunikasi tidak stabil
- **Penyebab Umum:** Kabel rusak, interface error, congestion, wireless interference
- **Gejala:** `ping` menunjukkan loss > 5%, TCP retransmission tinggi, voice/video stuttering
- **Solusi:** Ganti kabel, cek CRC error di interface, kurangi congestion

#### P12 - Latensi Tinggi / Jitter
- **Deskripsi:** Waktu respon sangat tinggi atau bervariasi
- **Penyebab Umum:** Congestion, routing tidak optimal, buffer bloat, wireless
- **Gejala:** Ping time > 100ms, variance besar, game/VoIP lag
- **Solusi:** Cek routing, aktifkan QoS, gunakan wired connection

### 3.6 Kategori: Keamanan & Firewall

#### P13 - Firewall Memblokir Koneksi
- **Deskripsi:** Aplikasi atau service tertentu tidak bisa berkomunikasi
- **Penyebab Umum:** Firewall rule terlalu ketat, port tertentu diblokir, IDS/IPS false positive
- **Gejala:** Aplikasi spesifik gagal connect, port tertentu filtered, error "connection refused"
- **Solusi:** Tambah exception di firewall, buka port yang diperlukan, review rule

### 3.7 Kategori: Hardware & Infrastruktur

#### P14 - Kerusakan Kabel / Konektor Jaringan
- **Deskripsi:** Kabel UTP/patch cord putus, konektor RJ45 longgar/rusak
- **Penyebab Umum:** Kabel terinjak, tergigit hewan, konektor aus, crimping buruk
- **Gejala:** Link lamp berkedip atau mati, packet loss saat kabel digerakkan, speed turun ke 10Mbps
- **Solusi:** Ganti kabel, re-crimp konektor, cek dengan cable tester

#### P15 - Kerusakan / Misconfiguration Router atau Switch
- **Deskripsi:** Perangkat jaringan (router/switch) bermasalah
- **Penyebab Umum:** Firmware bug, konfigurasi salah, overheating, power supply bermasalah
- **Gejala:** Semua client terdampak, VLAN salah, routing table error, device tidak respond
- **Solusi:** Restart device, update firmware, factory reset & reconfigure

---

## 4. Tabel Relasi Gejala - Masalah (Knowledge Base Matrix)

### 4.1 Daftar Gejala (Symptoms)

| Kode | Gejala | Pertanyaan ke User |
|------|--------|-------------------|
| G01 | Tidak ada koneksi sama sekali | "Apakah perangkat Anda tidak bisa terhubung ke jaringan sama sekali?" |
| G02 | Tidak bisa akses internet | "Apakah Anda tidak bisa membuka website atau aplikasi online?" |
| G03 | Bisa ping gateway tapi tidak bisa ping internet | "Apakah ping ke gateway berhasil tapi ping ke 8.8.8.8 gagal?" |
| G04 | Bisa ping IP publik tapi tidak bisa akses domain | "Apakah ping ke 8.8.8.8 berhasil tapi ping ke google.com gagal?" |
| G05 | IP address berupa 169.254.x.x | "Apakah IP address perangkat Anda dimulai dengan 169.254?" |
| G06 | Muncul pesan IP address conflict | "Apakah muncul notifikasi 'IP address conflict'?" |
| G07 | Subnet mask berbeda dari device lain | "Apakah subnet mask perangkat berbeda dari perangkat lain di jaringan?" |
| G08 | Tidak ada default gateway | "Apakah default gateway kosong atau 0.0.0.0?" |
| G09 | Tidak bisa connect ke WiFi | "Apakah perangkat gagal terhubung ke jaringan WiFi?" |
| G10 | SSID WiFi tidak muncul | "Apakah nama WiFi (SSID) tidak muncul di daftar jaringan?" |
| G11 | WiFi signal bar hanya 1-2 | "Apakah indikator signal WiFi hanya menunjukkan 1-2 bar?" |
| G12 | WiFi sering disconnect | "Apakah koneksi WiFi sering terputus?" |
| G13 | Kecepatan internet sangat lambat | "Apakah kecepatan internet jauh di bawah biasanya?" |
| G14 | Ping menunjukkan packet loss > 5% | "Apakah test ping menunjukkan paket hilang lebih dari 5%?" |
| G15 | Ping time sangat tinggi (>100ms lokal) | "Apakah ping ke server lokal menunjukkan waktu >100ms?" |
| G16 | Aplikasi tertentu tidak bisa connect | "Apakah hanya aplikasi tertentu yang gagal terhubung?" |
| G17 | Website redirect ke halaman aneh | "Apakah website yang biasa diakses mengarah ke halaman yang berbeda?" |
| G18 | Link lamp NIC/switch mati atau berkedip | "Apakah lampu indikator di port jaringan (NIC/switch) mati atau berkedip?" |
| G19 | Semua client di jaringan terdampak | "Apakah semua pengguna di jaringan mengalami masalah yang sama?" |
| G20 | Status NIC "Media Disconnected" | "Apakah status network adapter menunjukkan 'Media disconnected'?" |
| G21 | DNS server tidak respond saat nslookup | "Apakah perintah nslookup menunjukkan DNS server tidak merespon?" |
| G22 | Speed test menunjukkan hasil sangat rendah | "Apakah speed test menunjukkan kecepatan jauh di bawah paket ISP?" |
| G23 | Koneksi putus-nyala (intermittent) | "Apakah koneksi sering terputus lalu nyala kembali?" |
| G24 | Hanya bisa akses via IP, bukan domain | "Apakah Anda bisa mengakses website via IP tapi gagal via nama domain?" |
| G25 | Firewall/windows defender memblokir aplikasi | "Apakah firewall memblokir aplikasi yang ingin Anda gunakan?" |
| G26 | Device lain di jaringan yang sama normal | "Apakah perangkat lain di jaringan yang sama bisa normal?" |
| G27 | Koneksi normal setelah restart router | "Apakah masalah hilang sementara setelah me-restart router?" |
| G28 | Lampu WAN router merah | "Apakah lampu indikator WAN pada router berwarna merah?" |
| G29 | Kabel terlihat rusak atau longgar | "Apakah kabel jaringan terlihat rusak, terkelupas, atau konektor longgar?" |
| G30 | Device tidak mendapat IP DHCP | "Apakah perangkat tidak mendapatkan IP address secara otomatis?" |
| G31 | VPN tidak bisa connect | "Apakah VPN client gagal membuat koneksi?" |
| G32 | Koneksi VPN ada tapi resource internal tidak bisa diakses | "Apakah VPN terhubung tapi tidak bisa mengakses resource jaringan internal?" |
| G33 | Lampu LAN di router mati | "Apakah lampu indikator LAN pada router tidak menyala?" |
| G34 | Router tidak respond saat diakses | "Apakah Anda tidak bisa mengakses halaman admin router?" |
| G35 | Error "Destination Host Unreachable" saat ping | "Apakah muncul pesan 'Destination Host Unreachable' saat melakukan ping?" |
| G36 | Network adapter disabled | "Apakah network adapter dalam keadaan disabled?" |
| G37 | Driver network adapter bermasalah | "Apakah ada tanda seru kuning di Device Manager pada network adapter?" |
| G38 | Hanya satu perangkat yang bermasalah | "Apakah hanya perangkat Anda yang bermasalah, yang lain normal?" |
| G39 | Proxy setting aktif tanpa sepengetahuan | "Apakah ada setting proxy yang aktif di browser atau sistem?" |
| G40 | Error "Limited Connectivity" | "Apakah status koneksi menunjukkan 'Limited Connectivity'?" |

### 4.2 Matriks Gejala-Masalah

| Gejala | P01 | P02 | P03 | P04 | P05 | P06 | P07 | P08 | P09 | P10 | P11 | P12 | P13 | P14 | P15 |
|--------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| G01    | X   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| G02    |     | X   |     |     |     |     |     |     |     |     |     |     |     |     | X   |
| G03    |     | X   |     |     |     |     |     |     |     |     |     |     |     |     |     |
| G04    |     |     | X   |     |     |     |     |     |     |     |     |     |     |     |     |
| G05    |     |     |     |     | X   |     |     |     |     |     |     |     |     |     |     |
| G06    |     |     |     |     |     | X   |     |     |     |     |     |     |     |     |     |
| G07    |     |     |     |     |     |     | X   |     |     |     |     |     |     |     |     |
| G08    |     |     |     |     |     |     | X   |     |     |     |     |     |     |     |     |
| G09    |     |     |     |     |     |     |     | X   |     |     |     |     |     |     |     |
| G10    |     |     |     |     |     |     |     | X   |     |     |     |     |     |     |     |
| G11    |     |     |     |     |     |     |     |     | X   |     |     |     |     |     |     |
| G12    |     |     |     |     |     |     |     |     | X   |     |     |     |     |     |     |
| G13    |     |     |     |     |     |     |     |     |     | X   |     |     |     |     |     |
| G14    |     |     |     |     |     |     |     |     |     |     | X   |     |     | X   |     |
| G15    |     |     |     |     |     |     |     |     |     |     |     | X   |     |     |     |
| G16    |     |     |     |     |     |     |     |     |     |     |     |     | X   |     |     |
| G17    |     |     |     X   |     |     |     |     |     |     |     |     |     |     |     |     |
| G18    | X   |     |     |     |     |     |     |     |     |     |     |     |     | X   |     |
| G19    |     |     |     |     |     |     |     |     |     |     |     |     |     |     | X   |
| G20    | X   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| G21    |     |     | X   |     |     |     |     |     |     |     |     |     |     |     |     |
| G22    |     |     |     |     |     |     |     |     |     | X   |     |     |     |     |     |
| G23    |     |     |     |     |     | X   |     |     |     |     | X   |     |     | X   |     |
| G24    |     |     | X   |     |     |     |     |     |     |     |     |     |     |     |     |
| G25    |     |     |     |     |     |     |     |     |     |     |     |     | X   |     |     |
| G26    | X   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| G27    |     |     |     |     |     |     |     |     |     |     |     |     |     |     | X   |
| G28    |     | X   |     |     |     |     |     |     |     |     |     |     |     |     |     |
| G29    | X   |     |     |     |     |     |     |     |     |     |     |     |     | X   |     |
| G30    |     |     |     |     | X   |     |     |     |     |     |     |     |     |     |     |
| G31    |     |     |     |     |     |     |     |     |     |     |     |     | X   |     |     |
| G32    |     |     |     |     |     |     |     |     |     |     |     |     | X   |     |     |
| G33    |     |     |     |     |     |     |     |     |     |     |     |     |     | X   | X   |
| G34    |     |     |     |     |     |     |     |     |     |     |     |     |     |     | X   |
| G35    | X   |     |     |     |     |     | X   |     |     |     |     |     |     |     |     |
| G36    | X   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| G37    | X   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| G38    | X   |     |     |     |     |     |     | X   | X   |     |     |     |     |     |     |
| G39    |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| G40    |     |     |     |     | X   |     |     |     |     |     |     |     |     |     |     |

---

## 5. Aturan Inferensi (Rules)

### 5.1 Forward Chaining Rules (IF-THEN)

```
R01: IF G01 AND G20 AND G26
     THEN P01 (Tidak Ada Koneksi Jaringan)

R02: IF G02 AND G03 AND G28
     THEN P02 (Koneksi Internet Terputus)

R03: IF G04 AND G21 AND G24
     THEN P03 (DNS Resolution Failure)

R04: IF G17 AND G24
     THEN P04 (DNS Cache Poisoning/Hijacking)

R05: IF G05 AND G30 AND G40
     THEN P05 (DHCP Failure)

R06: IF G06 AND G23
     THEN P06 (IP Address Conflict)

R07: IF G07 AND G08 AND G35
     THEN P07 (Subnet Mask / Gateway Salah)

R08: IF G09 AND G10
     THEN P08 (Tidak Bisa Connect ke WiFi)

R09: IF G11 AND G12
     THEN P09 (WiFi Signal Lemah / Interferensi)

R10: IF G13 AND G22
     THEN P10 (Jaringan Lambat / Bandwidth Saturation)

R11: IF G14 AND G23
     THEN P11 (Packet Loss Tinggi)

R12: IF G15
     THEN P12 (Latensi Tinggi / Jitter)

R13: IF G16 AND G25
     THEN P13 (Firewall Memblokir Koneksi)

R14: IF G18 AND G29 AND G14
     THEN P14 (Kerusakan Kabel / Konektor)

R15: IF G19 AND G27 AND G34
     THEN P15 (Kerusakan / Misconfiguration Router-Switch)
```

### 5.2 Contoh Alur Forward Chaining

**Skenario:** User mengeluh tidak bisa browsing.

1. Sistem tanya: "Apakah Anda tidak bisa membuka website?" → User: Ya (G02 aktif)
2. Sistem tanya: "Apakah ping ke gateway berhasil tapi ping ke 8.8.8.8 gagal?" → User: Ya (G03 aktif)
3. Sistem tanya: "Apakah lampu indikator WAN pada router berwarna merah?" → User: Ya (G28 aktif)
4. Rule R02 terpicu: G02 AND G03 AND G28 → **P02 (Koneksi Internet Terputus)**
5. Sistem berikan solusi: Restart router, cek kabel WAN, hubungi ISP

---

## 6. Certainty Factor: Finalisasi Nilai MB/MD

### 6.1 Metodologi Penentuan MB/MD

**Formula dasar:**
```
CF[H,E] = MB[H,E] - MD[H,E]
```

- **MB (Measure of Belief):** Seberapa kuat gejala E mendukung hipotesis H (range 0-1)
- **MD (Measure of Disbelief):** Seberapa kuat gejala E menentang hipotesis H (range 0-1)
- **CF (Certainty Factor):** Nilai net keyakinan (range -1 sampai +1)

**Kriteria penentuan MB (kekuatan indikasi gejala terhadap masalah):**

| MB | Kategori | Kriteria |
|----|----------|----------|
| 0.9 | Sangat Kuat | Gejala hampir selalu muncul pada masalah ini (spesifik tinggi, >90%) |
| 0.8 | Kuat | Gejala sering muncul pada masalah ini (indikator kuat, ~80%) |
| 0.7 | Cukup Kuat | Gejala cukup sering muncul, indikator reliable (~70%) |
| 0.6 | Moderat | Gejala moderat, bisa muncul tapi tidak selalu (~60%) |
| 0.5 | Sedang | Gejala lumayan umum, ada kemungkinan (~50%) |
| 0.4 | Rendah-Sedang | Gejala lemah, bisa jadi indikasi tapi tidak pasti (~40%) |
| 0.3 | Rendah | Gejala mungkin saja muncul, tapi bisa dari masalah lain (~30%) |

**Kriteria penentuan MD (kemungkinan gejala TIDAK menunjukkan masalah ini):**

| MD | Kategori | Kriteria |
|----|----------|----------|
| 0.0 | Tidak ada | Gejala tidak pernah menentang masalah ini |
| 0.1 | Sangat Rendah | Hampir tidak ada kontra-indikasi |
| 0.2 | Rendah | Ada sedikit kemungkinan gejala ini dari masalah lain |
| 0.3 | Moderat | Gejala bisa datang dari beberapa masalah berbeda |

**Sumber penentuan:** Cross-referencing antara Cisco troubleshooting guide, CompTIA Network+ methodology, Microsoft network diagnostics, dan jurnal Indonesia yang sudah menggunakan CF pada domain jaringan.

### 6.2 Skala Keyakinan User

| Pilihan User | Nilai CF User |
|-------------|----------|
| Pasti Ya | 1.0 |
| Hampir Pasti Ya | 0.8 |
| Kemungkinan Besar Ya | 0.6 |
| Mungkin Ya | 0.4 |
| Tidak Tahu | 0.2 |
| Mungkin Tidak | -0.4 |
| Kemungkinan Besar Tidak | -0.6 |
| Hampir Pasti Tidak | -0.8 |
| Pasti Tidak | -1.0 |

### 6.3 Tabel MB/MD untuk Setiap Gejala per Masalah

Berikut adalah nilai MB dan MD untuk setiap kombinasi gejala-masalah. Nilai ditentukan berdasarkan seberapa spesifik gejala tersebut terhadap masalah yang bersangkutan.

#### P01 - Tidak Ada Koneksi Jaringan

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G01 - Tidak ada koneksi sama sekali | 0.9 | 0.1 | 0.8 | Gejala paling spesifik untuk P01, hampir pasti masalah konektivitas total |
| G20 - Status NIC Media Disconnected | 0.8 | 0.1 | 0.7 | Status ini langsung menunjukkan tidak ada link fisik |
| G26 - Device lain normal | 0.7 | 0.1 | 0.6 | Jika hanya perangkat sendiri, kemungkinan masalah lokal (NIC/kabel) |
| G18 - Link lamp mati/berkedip | 0.8 | 0.2 | 0.6 | Indikator kuat masalah fisik, tapi bisa juga switch port issue |
| G29 - Kabel terlihat rusak | 0.7 | 0.2 | 0.5 | Bukti visual kerusakan fisik, kuat tapi tidak selama terlihat |
| G35 - Destination Host Unreachable | 0.6 | 0.2 | 0.4 | Bisa berarti banyak hal, tapi mendukung P01 |
| G36 - Network adapter disabled | 0.9 | 0.0 | 0.9 | Penyebab langsung: adapter dimatikan |
| G37 - Driver bermasalah | 0.7 | 0.2 | 0.5 | Driver error bisa menyebabkan NIC tidak berfungsi |
| G38 - Hanya satu perangkat bermasalah | 0.6 | 0.1 | 0.5 | Mengarah ke masalah lokal, bukan infrastruktur |

#### P02 - Koneksi Internet Terputus

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G02 - Tidak bisa akses internet | 0.8 | 0.1 | 0.7 | Gejala utama P02, tapi bisa juga P03/P10 |
| G03 - Bisa ping gateway, gagal ping internet | 0.9 | 0.1 | 0.8 | Sangat spesifik: masalah di sisi WAN/ISP, bukan LAN |
| G28 - Lampu WAN router merah | 0.9 | 0.1 | 0.8 | Indikator kuat bahwa koneksi WAN down |

#### P03 - DNS Resolution Failure

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G04 - Bisa ping IP publik, gagal akses domain | 0.9 | 0.0 | 0.9 | Gejala pathognomonik DNS failure - sangat spesifik |
| G21 - DNS server tidak respond | 0.9 | 0.1 | 0.8 | Konfirmasi langsung DNS server bermasalah |
| G24 - Hanya bisa akses via IP, bukan domain | 0.9 | 0.0 | 0.9 | Gejala klasik DNS, hampir pasti masalah DNS |

#### P04 - DNS Cache Poisoning / Hijacking

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G17 - Website redirect ke halaman aneh | 0.8 | 0.3 | 0.5 | Indikator kuat, tapi bisa juga malware browser |
| G24 - Hanya bisa akses via IP, bukan domain | 0.6 | 0.1 | 0.5 | Juga gejala DNS biasa, jadi MB lebih rendah untuk P04 spesifik |

#### P05 - DHCP Failure

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G05 - IP address 169.254.x.x | 0.9 | 0.0 | 0.9 | APIPA address adalah tanda pasti DHCP failure |
| G30 - Device tidak mendapat IP DHCP | 0.9 | 0.1 | 0.8 | Definisi langsung dari DHCP failure |
| G40 - Limited Connectivity | 0.7 | 0.2 | 0.5 | Bisa juga karena masalah lain, tapi sering DHCP |

#### P06 - IP Address Conflict

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G06 - Pesan IP address conflict | 1.0 | 0.0 | 1.0 | Tanda pasti IP conflict, OS langsung mendeteksi |
| G23 - Koneksi putus-nyala | 0.6 | 0.3 | 0.3 | Gejala umum, bisa dari banyak masalah |

#### P07 - Subnet Mask / Default Gateway Salah

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G07 - Subnet mask berbeda | 0.9 | 0.0 | 0.9 | Gejala spesifik: langsung menunjukkan misconfig |
| G08 - Tidak ada default gateway | 0.8 | 0.1 | 0.7 | Gejala kuat: gateway kosong berarti tidak bisa routing |
| G35 - Destination Host Unreachable | 0.6 | 0.3 | 0.3 | Gejala umum, tidak spesifik untuk P07 saja |

#### P08 - Tidak Bisa Connect ke WiFi

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G09 - Tidak bisa connect WiFi | 0.8 | 0.1 | 0.7 | Gejala utama, tapi bisa juga P09 |
| G10 - SSID tidak muncul | 0.7 | 0.2 | 0.5 | Bisa berarti AP hidden, AP mati, atau adapter issue |
| G38 - Hanya satu perangkat bermasalah | 0.6 | 0.2 | 0.4 | Jika hanya satu device, kemungkinan client-side |

#### P09 - WiFi Signal Lemah / Interferensi

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G11 - WiFi signal bar 1-2 | 0.9 | 0.0 | 0.9 | Indikator langsung signal lemah |
| G12 - WiFi sering disconnect | 0.7 | 0.2 | 0.5 | Bisa juga dari interference, congestion, atau driver |

#### P10 - Jaringan Lambat / Bandwidth Saturation

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G13 - Kecepatan internet sangat lambat | 0.8 | 0.1 | 0.7 | Gejala utama, tapi bisa juga P11/P12 |
| G22 - Speed test sangat rendah | 0.9 | 0.0 | 0.9 | Pengukuran objektif, sangat spesifik |

#### P11 - Packet Loss Tinggi

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G14 - Packet loss > 5% | 0.9 | 0.0 | 0.9 | Definisi langsung packet loss |
| G23 - Koneksi putus-nyala | 0.5 | 0.3 | 0.2 | Gejala umum, banyak kemungkinan penyebab |

#### P12 - Latensi Tinggi / Jitter

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G15 - Ping time > 100ms lokal | 0.9 | 0.0 | 0.9 | Definisi langsung latensi tinggi |

#### P13 - Firewall Memblokir Koneksi

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G16 - Aplikasi tertentu gagal connect | 0.7 | 0.2 | 0.5 | Bisa juga DNS/routing, tapi firewall sering penyebab |
| G25 - Firewall memblokir aplikasi | 0.9 | 0.0 | 0.9 | Bukti langsung firewall blocking |
| G31 - VPN tidak bisa connect | 0.6 | 0.3 | 0.3 | Banyak penyebab VPN failure |
| G32 - VPN connect tapi resource tidak bisa diakses | 0.5 | 0.3 | 0.2 | Bisa routing/split-tunnel, bukan firewall pasti |

#### P14 - Kerusakan Kabel / Konektor

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G18 - Link lamp mati/berkedip | 0.7 | 0.2 | 0.5 | Indikator kuat kabel bermasalah |
| G29 - Kabel terlihat rusak | 0.9 | 0.0 | 0.9 | Bukti visual langsung |
| G14 - Packet loss > 5% | 0.5 | 0.3 | 0.2 | Bisa dari banyak penyebab, bukan kabel saja |
| G23 - Koneksi putus-nyala | 0.5 | 0.3 | 0.2 | Gejala umum |
| G33 - Lampu LAN router mati | 0.7 | 0.2 | 0.5 | Bisa kabel ATAU port router |

#### P15 - Kerusakan / Misconfiguration Router-Switch

| Gejala | MB | MD | CF (MB-MD) | Justifikasi |
|--------|----|----|------------|-------------|
| G19 - Semua client terdampak | 0.9 | 0.0 | 0.9 | Jika semua bermasalah, hampir pasti infrastruktur |
| G27 - Normal setelah restart router | 0.8 | 0.1 | 0.7 | Indikator kuat masalah di router |
| G34 - Router tidak respond | 0.9 | 0.0 | 0.9 | Router crash/hang, sangat spesifik |
| G33 - Lampu LAN router mati | 0.6 | 0.2 | 0.4 | Bisa juga kabel, bukan router pasti |
| G02 - Tidak bisa akses internet | 0.5 | 0.2 | 0.3 | Gejala umum |

### 6.4 Aturan dengan CF Values (Final)

Berikut adalah aturan IF-THEN lengkap beserta nilai MB/MD untuk setiap gejala dalam rule tersebut:

```
R01: IF G01(MB=0.9, MD=0.1) AND G20(MB=0.8, MD=0.1) AND G26(MB=0.7, MD=0.1)
     THEN P01 - Tidak Ada Koneksi Jaringan

R02: IF G02(MB=0.8, MD=0.1) AND G03(MB=0.9, MD=0.1) AND G28(MB=0.9, MD=0.1)
     THEN P02 - Koneksi Internet Terputus

R03: IF G04(MB=0.9, MD=0.0) AND G21(MB=0.9, MD=0.1) AND G24(MB=0.9, MD=0.0)
     THEN P03 - DNS Resolution Failure

R04: IF G17(MB=0.8, MD=0.3) AND G24(MB=0.6, MD=0.1)
     THEN P04 - DNS Cache Poisoning / Hijacking

R05: IF G05(MB=0.9, MD=0.0) AND G30(MB=0.9, MD=0.1) AND G40(MB=0.7, MD=0.2)
     THEN P05 - DHCP Failure

R06: IF G06(MB=1.0, MD=0.0) AND G23(MB=0.6, MD=0.3)
     THEN P06 - IP Address Conflict

R07: IF G07(MB=0.9, MD=0.0) AND G08(MB=0.8, MD=0.1) AND G35(MB=0.6, MD=0.3)
     THEN P07 - Subnet Mask / Gateway Salah

R08: IF G09(MB=0.8, MD=0.1) AND G10(MB=0.7, MD=0.2)
     THEN P08 - Tidak Bisa Connect ke WiFi

R09: IF G11(MB=0.9, MD=0.0) AND G12(MB=0.7, MD=0.2)
     THEN P09 - WiFi Signal Lemah / Interferensi

R10: IF G13(MB=0.8, MD=0.1) AND G22(MB=0.9, MD=0.0)
     THEN P10 - Jaringan Lambat / Bandwidth Saturation

R11: IF G14(MB=0.9, MD=0.0) AND G23(MB=0.5, MD=0.3)
     THEN P11 - Packet Loss Tinggi

R12: IF G15(MB=0.9, MD=0.0)
     THEN P12 - Latensi Tinggi / Jitter

R13: IF G16(MB=0.7, MD=0.2) AND G25(MB=0.9, MD=0.0)
     THEN P13 - Firewall Memblokir Koneksi

R14: IF G18(MB=0.7, MD=0.2) AND G29(MB=0.9, MD=0.0) AND G14(MB=0.5, MD=0.3)
     THEN P14 - Kerusakan Kabel / Konektor

R15: IF G19(MB=0.9, MD=0.0) AND G27(MB=0.8, MD=0.1) AND G34(MB=0.9, MD=0.0)
     THEN P15 - Kerusakan / Misconfiguration Router-Switch
```

### 6.5 Contoh Perhitungan CF Lengkap

#### Skenario 1: User Tidak Bisa Browsing (P02)

User memilih gejala dengan tingkat keyakinan berikut:
- G02 (Tidak bisa akses internet): "Hampir Pasti Ya" → CF_user = 0.8
- G03 (Bisa ping gateway, gagal ping internet): "Pasti Ya" → CF_user = 1.0
- G28 (Lampu WAN router merah): "Kemungkinan Besar Ya" → CF_user = 0.6

**Step 1: Hitung CF(H,E) untuk setiap gejala**
```
CF(G02→P02) = MB - MD = 0.8 - 0.1 = 0.7
CF(G03→P02) = MB - MD = 0.9 - 0.1 = 0.8
CF(G28→P02) = MB - MD = 0.9 - 0.1 = 0.8
```

**Step 2: Hitung CF evidence per gejala**
```
CF_evidence(G02) = CF_user × CF(H,E) = 0.8 × 0.7 = 0.56
CF_evidence(G03) = CF_user × CF(H,E) = 1.0 × 0.8 = 0.80
CF_evidence(G28) = CF_user × CF(H,E) = 0.6 × 0.8 = 0.48
```

**Step 3: Kombinasikan dengan rumus CF_combine**
```
CF[1,2] = CF1 + CF2 × (1 - CF1)
        = 0.56 + 0.80 × (1 - 0.56)
        = 0.56 + 0.352
        = 0.912

CF[2,3] = CF[1,2] + CF3 × (1 - CF[1,2])
        = 0.912 + 0.48 × (1 - 0.912)
        = 0.912 + 0.0422
        = 0.954
```

**Hasil:** P02 (Koneksi Internet Terputus) dengan keyakinan **95.4%**

#### Skenario 2: WiFi Bermasalah (P09)

User memilih:
- G11 (WiFi signal bar 1-2): "Kemungkinan Besar Ya" → CF_user = 0.6
- G12 (WiFi sering disconnect): "Mungkin Ya" → CF_user = 0.4

**Step 1: CF(H,E)**
```
CF(G11→P09) = 0.9 - 0.0 = 0.9
CF(G12→P09) = 0.7 - 0.2 = 0.5
```

**Step 2: CF evidence**
```
CF_evidence(G11) = 0.6 × 0.9 = 0.54
CF_evidence(G12) = 0.4 × 0.5 = 0.20
```

**Step 3: Kombinasi**
```
CF[1,2] = 0.54 + 0.20 × (1 - 0.54)
        = 0.54 + 0.092
        = 0.632
```

**Hasil:** P09 (WiFi Signal Lemah) dengan keyakinan **63.2%**

#### Skenario 3: Semua Mati (P15)

User memilih:
- G19 (Semua client terdampak): "Pasti Ya" → CF_user = 1.0
- G27 (Normal setelah restart router): "Hampir Pasti Ya" → CF_user = 0.8
- G34 (Router tidak respond): "Pasti Ya" → CF_user = 1.0

**Step 1: CF(H,E)**
```
CF(G19→P15) = 0.9 - 0.0 = 0.9
CF(G27→P15) = 0.8 - 0.1 = 0.7
CF(G34→P15) = 0.9 - 0.0 = 0.9
```

**Step 2: CF evidence**
```
CF_evidence(G19) = 1.0 × 0.9 = 0.90
CF_evidence(G27) = 0.8 × 0.7 = 0.56
CF_evidence(G34) = 1.0 × 0.9 = 0.90
```

**Step 3: Kombinasi**
```
CF[1,2] = 0.90 + 0.56 × (1 - 0.90) = 0.90 + 0.056 = 0.956
CF[2,3] = 0.956 + 0.90 × (1 - 0.956) = 0.956 + 0.0396 = 0.996
```

**Hasil:** P15 (Kerusakan Router-Switch) dengan keyakinan **99.6%**

### 6.6 Interpretasi Hasil CF

| Range CF Final | Interpretasi | Tindakan Sistem |
|----------------|-------------|-----------------|
| 0.80 - 1.00 | Sangat Yakin | Tampilkan diagnosis utama + solusi langsung |
| 0.60 - 0.79 | Cukup Yakin | Tampilkan diagnosis + minta konfirmasi user |
| 0.40 - 0.59 | Kemungkinan | Tampilkan sebagai "kemungkinan" + saran gejala tambahan |
| 0.20 - 0.39 | Kurang Yakin | Tampilkan sebagai "mungkin" + rekomendasi cek lebih lanjut |
| < 0.20 | Tidak Yakin | Minta user pilih gejala tambahan / konsultasi teknisi |

### 6.7 Catatan Penting tentang CF Values

1. **Nilai MB/MD bersifat heuristic** - ditentukan berdasarkan dokumentasi teknis, bukan statistik formal. Untuk keperluan UAS, ini sudah memadai.
2. **CF bisa di-tuning** - setelah implementasi, nilai dapat disesuaikan berdasarkan hasil testing terhadap skenario yang sudah diketahui jawabannya.
3. **Prinsip konservatif** - MB cenderung tinggi (0.7-0.9) untuk gejala spesifik, dan MD rendah (0.0-0.3) karena sebagian besar gejala memang mendukung masalah terkait.
4. **Gejala ambigu** (muncul di beberapa masalah) memiliki MB lebih rendah dan MD lebih tinggi - ini memungkinkan sistem membedakan antar masalah yang mirip.

---

## 7. Arsitektur Sistem yang Direncanakan

```
+---------------------------------------------------------+
|                    USER INTERFACE (Web)                   |
|  [Pilih Gejala] → [Tingkat Keyakinan] → [Hasil Diagnosis]|
+---------------------------------------------------------+
                           |
+---------------------------------------------------------+
|                  KNOWLEDGE BASE (JSON/DB)                |
|  - 15 Masalah Jaringan (Diseases)                       |
|  - 40 Gejala (Symptoms)                                 |
|  - 15+ Aturan IF-THEN + CF values                       |
+---------------------------------------------------------+
                           |
+---------------------------------------------------------+
|                  INFERENCE ENGINE                        |
|  [Forward Chaining] + [Certainty Factor Calculation]    |
+---------------------------------------------------------+
                           |
+---------------------------------------------------------+
|                  WORKING MEMORY                          |
|  - Facts (gejala yang dipilih + CF user)               |
|  - Intermediate results                                  |
+---------------------------------------------------------+
```

### Tech Stack yang Direncanakan

| Komponen | Teknologi |
|----------|-----------|
| Frontend | HTML + CSS + JavaScript (atau Flask template) |
| Backend | Python (Flask) |
| Knowledge Base | JSON file atau SQLite |
| Inference Engine | Python custom (FC + CF logic) |
| Deployment | Local / PythonAnywhere / GitHub Pages |

---

## 8. Perbandingan dengan Implementasi Sebelumnya (Jurnal)

| Aspek | Jurnal Indihome (Sya'i, 2022) | Jurnal LAN (Nurmanta, 2020) | **Rencana Kita** |
|-------|-------------------------------|------------------------------|------------------|
| Metode | Forward Chaining | FC + Certainty Factor | FC + Certainty Factor |
| Jumlah Masalah | 15 gangguan | 10 gangguan | 15 masalah |
| Jumlah Gejala | ~18 gejala | ~25 gejala | 40 gejala |
| Platform | Web (PHP+MySQL) | Web | Web (Python Flask) |
| Basis Pengetahuan | MySQL | Database | JSON/SQLite |
| Akurasi | N/A | ~85% | Target 85%+ |

---

## 9. Referensi

### Jurnal Indonesia
1. Sya'i, M., et al. (2022). "Sistem Pakar untuk Mendeteksi Kerusakan Jaringan Internet pada Indihome di Pematangsiantar." *JIKI*, Vol. 2, No. 1, hal 37-46.
2. Nurmanta, A. & Fachrie, M. (2020). "Sistem Pakar Diagnosis Gangguan Pada Jaringan LAN Menggunakan Metode Forward Chaining dan Certainty Factor."
3. Asnawi, M.F. & Sunarto, Y.Y. (2021). "Sistem Pakar Troubleshooting Jaringan Komputer Menggunakan Metode Certainty Factor." *Device*, 11(2), 39-47.
4. Aplikasi Sistem Pakar Diagnosa Troubleshooting Jaringan LAN. *Jurnal Infotech STTM Cileungsi* (2023).
5. Aplikasi Sistem Pakar Diagnosa Kegagalan Koneksi TCP/IP. *Prosiding SENATIK UNIPMA*.

### Sumber Teknis Internasional
6. Obkio. "16 Most Common Network Problems: How to Find & Fix Them." https://obkio.com/blog/common-network-problems/
7. NinjaOne. "8 Common Network Issues & How To Fix Them." https://www.ninjaone.com/blog/common-network-issues/
8. PyNet Labs. "10 Common Network Issues and How to Solve Them." https://www.pynetlabs.com/network-issues-and-their-solutions/
9. NetworkCheckr. "Troubleshoot Network Connectivity: 7-Step Guide." https://networkcheckr.com/how-to-troubleshoot-network-connectivity/
10. IEEE Xplore. "Expert Diagnosis Systems for Network Connection Problems." https://ieeexplore.ieee.org/document/7102428/
11. IEEE Xplore. "AILAN: a local area network diagnostic expert system." https://ieeexplore.ieee.org/document/302274/

### Textbook
12. Negnevitsky, M. (2024). *Artificial Intelligence: A Guide to Intelligent Systems.* 4th Ed. Chapter 2-5: Rule-Based Expert Systems.
13. Kusumadewi, S. (2003). *Artificial Intelligence.* Bab 5: Sistem Pakar.

---

## 10. Next Actions

1. [x] Riset mendalam domain troubleshooting jaringan
2. [x] Kompilasi daftar masalah jaringan (15 masalah)
3. [x] Kompilasi daftar gejala (40 gejala)
4. [x] Buat knowledge base matrix
5. [x] Definisikan aturan IF-THEN
6. [x] Finalisasi CF values (MB/MD) untuk setiap aturan
7. [ ] Implementasi sistem (code)
8. [ ] Testing dan validasi
9. [ ] Dokumentasi laporan

---

*File ini merupakan kelanjutan dari riset perbandingan sistem pakar pada tanggal 2026-06-05. Domain troubleshooting jaringan komputer dipilih berdasarkan rekomendasi TOP 3 dari dokumen perbandingan.*
