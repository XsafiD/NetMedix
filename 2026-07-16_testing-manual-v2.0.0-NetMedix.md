---
created_at: 2026-07-16
version: "2.0.0"
project: "NetMedix"
topic: "Tasklist Testing Manual NetMedix v2.0.0"
tags: [netmedix, testing, manual, qa, v2.0.0, tasklist]
related_files:
  - "[TODO rombak v2.0.0](../todo-rombak-v2.0.0-NetMedix.md)"
  - "[Perencanaan v2.0.0](../perencanaan-rombak-v2.0.0-NetMedix.md)"
  - "[Desain teknis v2.0.0](../desain-teknis-v2.0.0-NetMedix.md)"
status: "ready"
suggested_location: "04_TUGAS/NetMedix"
ai_model: "Claude (glm-4.7)"
---

# Tasklist Testing Manual NetMedix v2.0.0

> Dokumen panduan testing manual untuk NetMedix v2.0.0. Gunakan tasklist ini untuk memverifikasi semua fitur berfungsi dengan baik sebelum deployment.

---

## Cara Menggunakan Tasklist Ini

### Format Test Case

```markdown
### [TEST-ID] Nama Test

**Tujuan:** Tujuan testing ini

**Prasyarat:**
- Server Flask berjalan di `localhost:5000`
- Database SQLite terinisialisasi

**Steps:**
1. Langkah pertama
2. Langkah kedua
...

**Expected Result:**
- Hasil yang diharapkan

**Actual Result:**
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

**Notes:**
Catatan tambahan jika ada...
```

### Status Legend

- `[ ]` — Belum ditest
- `[x]` — PASS
- `[!]` — FAIL
- `[~]` — BLOCKED (ada blocker)

---

## TEST-01: Setup & Environment Check

### Tujuan
Memastikan environment siap untuk testing

### Prasyarat
- Python 3 terinstall
- Dependensi terinstall (Flask, dll)

### Steps
1. Cek Python version: `python3 --version`
2. Navigasi ke project directory: `cd /path/to/NetMedix`
3. Cek apakah `data/` folder exists dan berisi file JSON
4. Cek apakah `inference/` folder exists dan berisi engine files
5. Start Flask server: `python3 app.py`
6. Buka browser: `http://localhost:5000`

### Expected Result
- Python 3.x terinstall
- Folder `data/`, `inference/`, `templates/` exists
- File `rules.json`, `symptoms.json`, `problems.json` exists
- Flask server berjalan tanpa error
- Halaman home terbuka di browser

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-02: Halaman Home (Index Page)

### Tujuan
Memastikan halaman home menampilkan semua elemen dengan benar

### Prasyarat
- Flask server berjalan di `localhost:5000`

### Steps
1. Buka `http://localhost:5000`
2. Cek heading utama: "NetMedix"
3. Cek subheading: "Diagnosis Jaringan Komputer"
4. Cek tombol "Mulai Diagnosis" ada dan clickable
5. Cek navigasi: Diagnosis, Riwayat, Tentang, Admin
6. Cek logo/branding elements
7. Cek responsive layout (resize browser window)

### Expected Result
- Heading "NetMedix" terlihat dengan warna primary
- Subheading "Diagnosis Jaringan Komputer" terlihat
- Tombol "Mulai Diagnosis" terlihat dengan background hijau (primary) dan text putih
- Menu navigasi: Diagnosis, Riwayat, Tentang, Admin
- Responsive layout: menu stack properly di mobile
- Tidak ada console error (buka DevTools → Console)

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-03: Halaman Diagnosis — Step 1 (Pilih Gejala)

### Tujuan
Memastikan halaman pemilihan gejala berfungsi dengan benar

### Prasyarat
- Flask server berjalan

### Steps
1. Buka `http://localhost:5000`
2. Klik tombol "Mulai Diagnosis"
3. Cek URL berubah menjadi `/diagnose`
4. Cek heading: "LANGKAH 1 — Pilih Gejala"
5. Cek list gejala (G01-G40) ditampilkan
6. Cek tombol info ⓘ di samping setiap gejala
7. Pilih beberapa gejala (contoh: G02, G03, G28)
8. Klik tombol ⓘ pada salah satu gejala

### Expected Result
- URL: `http://localhost:5000/diagnose`
- Heading "LANGKAH 1 — Pilih Gejala" terlihat
- 40 gejala ditampilkan dalam kategori (Hardware, Software, Koneksi, Performa, DNS, Lainnya)
- Setiap gejala punya checkbox dan tombol ⓘ
- Tombol ⓘ clickable dan membuka modal info
- Modal info menampilkan: kode gejala, nama, short_desc, how_to_check
- Modal ada link "Pelajari lebih lanjut →"
- Modal bisa ditutup dengan tombol "Tutup" atau klik di luar modal

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-04: Tutorial Gejala (Modal Info Link)

### Tujuan
Memastikan halaman tutorial gejala berfungsi dengan benar

### Prasyarat
- Halaman diagnosis Step 1 terbuka

### Steps
1. Dari halaman diagnosis Step 1
2. Klik tombol ⓘ pada gejala G01
3. Klik link "Pelajari lebih lanjut →"
4. Cek halaman `/tutorial/G01` terbuka
5. Baca konten tutorial: definisi, cara verifikasi, interpretasi, penyebab umum
6. Cek link ke gejala terkait

### Expected Result
- URL: `http://localhost:5000/tutorial/G01`
- Heading menampilkan kode dan nama gejala
- Section terlihat: Definisi, Cara Verifikasi, Interpretasi Hasil, Penyebab Umum, Gejala Terkait
- Layout YAML-like dengan dark header
- Tombol "← Kembali ke form" ada dan clickable
- Link gejala terkait clickable dan mengarah ke `/tutorial/GXX`
- Responsive layout berfungsi

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-05: Halaman Diagnosis — Step 2 (Input CF User)

### Tujuan
Memastikan halaman input CF user berfungsi dengan benar

### Prasyarat
- Beberapa gejala sudah dipilih di Step 1

### Steps
1. Dari halaman diagnosis Step 1
2. Pilih minimal 2 gejala (contoh: G02, G03, G28)
3. Klik tombol "Lanjut"
4. Cek URL berubah menjadi `/diagnose/step2`
5. Cek heading: "LANGKAH 2 — Tentukan Keyakinan"
6. Cek gejala yang dipilih ditampilkan dengan radio button 5 level
7. Cek label radio: 0.1 (Hampir Tidak Yakin), 0.3 (Kurang Yakin), 0.5 (Cukup Yakin), 0.7 (Yakin), 1.0 (Sangat Yakin)
8. Cek default value: 0.5 (Cukup Yakin) pre-checked
9. Ubah CF user untuk beberapa gejala
10. Klik tombol "Kembali" untuk kembali ke Step 1
11. Klik tombol "Lihat Diagnosis"

### Expected Result
- URL: `http://localhost:5000/diagnose/step2`
- Heading "LANGKAH 2 — Tentukan Keyakinan" terlihat
- Gejala yang dipilih ditampilkan dengan radio button 5 level
- Label 5 level CF terlihat jelas
- Default value 0.5 pre-checked untuk semua gejala
- Radio button clickable dan mengubah selection
- Tombol "Kembali" navigasi kembali ke Step 1 dengan memilih gejala yang sama
- Tombol "Lihat Diagnosis" navigasi ke halaman result
- Responsive: radio button stack di mobile (≤375px)

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-06: Halaman Hasil Diagnosis (Result Page)

### Tujuan
Memastikan halaman hasil diagnosis menampilkan informasi dengan benar

### Prasyarat
- Step 2 completed dengan gejala dan CF user terisi

### Steps
1. Dari halaman diagnosis Step 2
2. Submit diagnosis dengan klik "Lihat Diagnosis"
3. Cek URL berubah menjadi `/result`
4. Cek Section Kesimpulan di bagian atas
5. Cek nama problem utama terdeteksi
6. Cek persentase keyakinan (percentage)
7. Cek label (Sangat Yakin, Yakin, dll)
8. Scroll ke bawah ke Section Detail Kandidat
9. Cek semua kandidat ditampilkan (bukan top-3 saja)
10. Klik "Lihat trace perhitungan" pada salah satu kandidat
11. Cek tabel evidence_steps
12. Cek tabel combine_steps

### Expected Result
- URL: `http://localhost:5000/result`
- Section Kesimpulan ada di atas
- Problem utama terdeteksi dengan nama jelas
- Persentase ditampilkan dalam format X%
- Label sesuai: Sangat Yakin (≥70%), Yakin (50-69%), Cukup Yakin (30-49%), Kurang Yakin (10-29%), Hampir Tidak Yakin (<10%)
- Section Detail Kandidat menampilkan SEMUA kandidat yang lolos filter ≥ 2 gejala
- Setiap kandidat punya card dengan: code, name, percentage badge, matched_count
- Trace Perhitungan collapsible dengan details:
  - Evidence steps: Symptom | CF_pakar | CF_user | CF_evidence
  - Evidence note (justifikasi pakar) ditampilkan
  - Combine steps: Step | CFₐ | CFᵦ | Result
- Tombol "Diagnosis Lagi" navigasi kembali ke halaman home

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-07: Skenario Diagnosis — P02 (Internet Putus)

### Tujuan
Testing diagnosis untuk problem spesifik: P02 Koneksi Internet Terputus

### Prasyarat
- Knowledge base loaded dengan rule R02

### Steps
1. Buka `http://localhost:5000`
2. Klik "Mulai Diagnosis"
3. Pilih gejala: G02 (Tidak bisa akses internet), G03 (Browser timeout), G28 (Modem/router restart)
4. Klik "Lanjut"
5. Set CF_user: G02=1.0, G03=1.0, G28=0.8
6. Klik "Lihat Diagnosis"

### Expected Result
- Top result: **P02 — Koneksi Internet Terputus**
- Percentage: ≥ 85% (high confidence karena 3 gejala signature dengan CF tinggi)
- Label: "Sangat Yakin" atau "Yakin"
- Evidence steps menampilkan:
  - G02: CF_pakar ~0.90, CF_user 1.0 → CF_evidence ~0.90
  - G03: CF_pakar ~0.85, CF_user 1.0 → CF_evidence ~0.85
  - G28: CF_pakar ~0.70, CF_user 0.8 → CF_evidence ~0.56
- Combine steps menampilkan kombinasi CF yang benar
- Matched count: 3/3 atau sesuai rule R02

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-08: Skenario Diagnosis — P05 (DHCP Failure)

### Tujuan
Testing diagnosis untuk problem spesifik: P05 DHCP Failure

### Prasyarat
- Knowledge base loaded dengan rule R05

### Steps
1. Buka `http://localhost:5000`
2. Klik "Mulai Diagnosis"
3. Pilih gejala: G05 (IP address 169.254.x.x), G30 (DHCP request timeout), G40 (Tidak dapat IP via DHCP)
4. Klik "Lanjut"
5. Set CF_user: G05=1.0, G30=0.9, G40=1.0
6. Klik "Lihat Diagnosis"

### Expected Result
- Top result: **P05 — DHCP Failure**
- Percentage: ≥ 80% (high confidence)
- Label: "Sangat Yakin" atau "Yakin"
- Evidence steps menampilkan 3 gejala dengan CF_pakar yang sesuai
- Combine steps menampilkan perhitungan kombinasi yang benar
- Tidak ada problem lain dengan percentage tinggi

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-09: Skenario Edge Case — < 2 Gejala

### Tujuan
Testing behavior ketika user memilih < 2 gejala (gagal filter)

### Prasyarat
- Flask server berjalan

### Steps
1. Buka `http://localhost:5000`
2. Klik "Mulai Diagnosis"
3. Pilih hanya 1 gejala: G02 saja
4. Klik "Lanjut"
5. Set CF_user: G02=0.7
6. Klik "Lihat Diagnosis"

### Expected Result
- Halaman result menampilkan **empty state**
- Pesan: "Tidak ada diagnosis yang memenuhi syarat (minimal 2 gejala relevan). Coba pilih gejala tambahan yang lebih spesifik."
- Tidak ada kandidat diagnosis yang muncul
- Tombol "Diagnosis Lagi" ada untuk mencoba lagi

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-10: Skenario Edge Case — 0 Gejala

### Tujuan
Testing behavior ketika user memilih 0 gejala

### Prasyarat
- Flask server berjalan

### Steps
1. Buka `http://localhost:5000`
2. Klik "Mulai Diagnosis"
3. Jangan pilih gejala manapun
4. Klik "Lanjut"

### Expected Result
- Form validation muncul: "Pilih minimal 1 gejala dulu"
- Atau otomatis redirect kembali ke Step 1 dengan pesan error
- Tidak bisa lanjut ke Step 2 tanpa memilih gejala

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-11: Halaman Riwayat Diagnosis

### Tujuan
Memastikan halaman riwayat berfungsi dengan benar

### Prasyarat
- Minimal 1 diagnosis sudah dilakukan
- Database SQLite exists

### Steps
1. Buka `http://localhost:5000`
2. Klik menu "Riwayat" di navigasi
3. Cek URL berubah menjadi `/history`
4. Cek list riwayat diagnosis ditampilkan
5. Cek setiap entry menampilkan: timestamp, gejala yang dipilih, hasil diagnosis
6. Klik salah satu entry riwayat untuk melihat detail
7. Cek tombol "Hapus Riwayat" (jika ada)

### Expected Result
- URL: `http://localhost:5000/history`
- Heading "Riwayat Diagnosis" terlihat
- List riwayat ditampilkan dalam tabel atau cards
- Setiap entry menampilkan:
  - Timestamp dalam format yang readable
  - Count gejala yang dipilih
  - Top result problem dengan percentage
- Entry lama (v1.0.0 schema jika ada) tetap ter-render dengan fallback
- Tombol "Hapus Riwayat" (jika ada) menghapus semua riwayat
- Tombol "Kembali" atau navigasi kembali ke home

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-12: Halaman Admin — Login

### Tujuan
Memastikan halaman admin login berfungsi (kalau fitur admin ada)

### Prasyarat
- Flask server berjalan
- Fitur admin enabled

### Steps
1. Buka `http://localhost:5000/admin`
2. Cek halaman login muncul
3. Cek field username dan password
4. Cek tombol "Login"
5. (Kalau tahu credentials) Login dengan username/password

### Expected Result
- URL: `http://localhost:5000/admin`
- Heading "Admin Login" terlihat
- Form login dengan field username dan password
- Tombol "Login" clickable
- Jika credentials salah: muncul pesan error
- Jika credentials benar: redirect ke dashboard admin

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-13: Halaman Admin — CRUD Rules (Optional)

### Tujuan
Testing fitur admin untuk CRUD rules (kalau ada)

### Prasyarat
- Sudah login sebagai admin

### Steps
1. Dari dashboard admin
2. Klik menu "Rules"
3. Cek list rules (R01-R15) ditampilkan
4. Cek tombol "Add New Rule" (jika ada)
5. Cek tombol "Edit" pada salah satu rule
6. Cek tombol "Delete" pada salah satu rule (optional, hati-hati)

### Expected Result
- List 15 rules ditampilkan dengan code, name, target problem
- Setiap rule punya gejala dengan CF_pakar
- Tombol Edit/Delete ada (kalau fitur CRUD ada)
- Edit menampilkan form dengan field CF_pakar, evidence, sources
- Perubahan tersimpan ke database/file JSON

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-14: Halaman Tentang (About)

### Tujuan
Memastikan halaman About menampilkan informasi dengan benar

### Prasyarat
- Flask server berjalan

### Steps
1. Buka `http://localhost:5000`
2. Klik menu "Tentang"
3. Cek URL berubah menjadi `/about`
4. Baca konten tentang NetMedix
5. Cek informasi versi (seharusnya v2.0.0)

### Expected Result
- URL: `http://localhost:5000/about`
- Heading "Tentang NetMedix" terlihat
- Konten menjelaskan:
  - Apa itu NetMedix
  - Metodologi Certainty Factor
  - Jumlah gejala (40) dan problem (15)
- Versi tertera: NetMedix v2.0.0
- Responsive layout berfungsi

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-15: Responsive Design — Mobile (375px)

### Tujuan
Memastikan aplikasi berfungsi dengan baik di mobile

### Prasyarat
- Browser dengan DevTools (Chrome/Firefox)

### Steps
1. Buka DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M / Cmd+Shift+M)
3. Pilih device: iPhone SE atau custom 375x667
4. Buka `http://localhost:5000`
5. Cek halaman home tidak ada horizontal overflow
6. Cek menu mobile hamburger berfungsi
7. Navigasi ke halaman diagnosis
8. Cek list gejala readable di mobile
9. Cek tombol/info button clickable (min 44x44px)
10. Navigasi ke halaman result
11. Cek table trace tidak overflow horizontal

### Expected Result
- Tidak ada horizontal overflow di semua halaman
- Menu navigasi mobile berfungsi dengan hamburger menu
- Typography readable (tidak terlalu kecil)
- Touch targets min 44x44px untuk button/checkbox
- Table di halaman result stack atau scrollable di mobile
- Modal info responsive di layar kecil
- Radio button 5 level stack di mobile (≤375px)

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-16: Accessibility Check (Keyboard Navigation)

### Tujuan
Memastikan aplikasi accessible via keyboard

### Prasyarat
- Browser terbuka

### Steps
1. Buka `http://localhost:5000`
2. Gunakan Tab key untuk navigasi
3. Cek focus order logical
4. Cek focus indicator visible (outline/glow)
5. Tekan Enter pada button yang ter-focus
6. Cek Enter/Space pada checkbox dan radio button
7. Cek Escape key untuk menutup modal

### Expected Result
- Tab navigation berjalan dengan urutan logical: menu → button → form fields
- Focus indicator jelas terlihat (outline hijau sesuai CSS)
- Enter/Space mengaktifkan button/checkbox/radio
- Escape menutup modal info
- Tidak ada keyboard trap (user bisa keluar dari semua komponen)

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-17: Color Contrast Check

### Tujuan
Verifikasi color contrast memenuhi standar WCAG AA

### Prasyarat
- Browser terbuka

### Steps
1. Buka semua halaman utama: home, diagnosis step1, step2, result, tutorial, history, about
2. Cek text pada background putih (canvas)
3. Cek tombol primary (background hijau, text putih)
4. Cek link dan label
5. (Optional) Gunakan color contrast checker tool atau Lighthouse

### Expected Result
- Text-ink (#171717) pada background-white (#ffffff): kontras ≥ 4.5:1 ✅
- Text-primary (#047857) pada background-white: kontras ≥ 4.5:1 ✅
- Text-ink-mute (#707070) pada background-white: kontras ≥ 4.5:1 ✅
- Text-white (#ffffff) pada background-primary (#047857): kontras ≥ 4.5:1 ✅
- Tidak ada text yang sulit dibaca
- Lighthouse Accessibility score: 100 ✅

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-18: Performance Check — Load Time

### Tujuan
Memastikan aplikasi load dalam waktu reasonable

### Prasyarat
- Browser dengan DevTools

### Steps
1. Buka DevTools (F12)
2. Tab Network
3. Clear cache
4. Buka `http://localhost:5000`
5. Cek timing: DOMContentLoaded, Load
6. Navigasi ke halaman lain
7. Cek page load time untuk setiap halaman

### Expected Result
- Home page load: < 2 detik (ideal)
- Diagnosis pages: < 1 detik
- Result page: < 1 detik
- Tutorial page: < 1 detik
- Total resource size reasonable (< 500KB untuk HTML+CSS+JS)
- Tidak ada resource yang gagal load (404/500 error)

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-19: Error Handling — 404 Page

### Tujuan
Memastikan halaman 404 menampilkan dengan benar

### Prasyarat
- Flask server berjalan

### Steps
1. Buka URL yang tidak ada: `http://localhost:5000/page-tidak-ada`
2. Cek halaman 404 muncul

### Expected Result
- Halaman 404 terdeteksi (bukan browser default error)
- Pesan error friendly: "Halaman tidak ditemukan"
- Tombol "Kembali" atau link ke home
- Status HTTP 404 di DevTools Network tab
- Responsive layout berfungsi

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-20: Error Handling — Tutorial Orphan Symptoms

### Tujuan
Memastikan halaman tutorial untuk gejala orphan (G31, G32) menampilkan dengan benar

### Prasyarat
- Flask server berjalan

### Steps
1. Buka `http://localhost:5000/tutorial/G31`
2. Cek halaman 404 muncul (karena G31 VPN out-of-scope)
3. Buka `http://localhost:5000/tutorial/G32`
4. Cek halaman 404 muncul (karena G32 VPN out-of-scope)

### Expected Result
- Halaman 404 untuk gejala yang tidak didukung (G31, G32)
- Atau halaman tutorial dengan pesan "Gejala ini belum didukung sistem diagnosis"
- Tidak ada crash/error server (HTTP 500)

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-21: Database Check — History Persistence

### Tujuan
Memastikan riwayat diagnosis tersimpan di database

### Prasyarat
- Flask server berjalan

### Steps
1. Buka `http://localhost:5000`
2. Lakukan diagnosis dengan gejala apapun
3. Submit diagnosis
4. Cek riwayat: `http://localhost:5000/history`
5. Verifikasi entry baru muncul
6. Restart Flask server
7. Buka riwayat lagi
8. Verifikasi entry masih ada (persistent)

### Expected Result
- Entry diagnosis muncul di halaman riwayat
- Entry berisi timestamp, gejala yang dipilih, hasil diagnosis
- Entry tetap ada setelah server restart (persistent di SQLite)
- Database file `netmedix.db` ada di folder project

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-22: Cross-Cutting Symptoms Test

### Tujuan
Testing symptoms yang muncul di multiple rules (cross-cutting)

### Prasyarat
- Knowledge base loaded

### Steps
1. Buka `http://localhost:5000`
2. Lakukan diagnosis dengan: G14 (Packet loss), G23 (Intermittent), G18 (Kabel rusak), G29 (Kabel longgar)
3. Set CF_user: semua 0.9
4. Submit diagnosis

### Expected Result
- Dua problem muncul (karena gejala cross-cutting):
  - **P11 — Packet Loss Tinggi** (G14 + G23)
  - **P14 — Kerusakan Kabel** (G18 + G29 + G14)
- Keduanya muncul dengan percentage tinggi
- P11 dan P14 sorted desc by CF (CF tinggi di atas)
- Evidence steps menampilkan kombinasi gejala yang benar untuk setiap problem

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-23: CF Range Validation

### Tujuan
Memastikan CF_user yang diinput valid dalam range [0.1, 1.0]

### Prasyarat
- Flask server berjalan

### Steps
1. Buka browser DevTools → Console
2. Lakukan diagnosis sampai Step 2
3. Di Console, manipulasi CF value: ubah menjadi 2.0 atau -0.5
4. Submit diagnosis
5. Cek result

### Expected Result
- Backend clamps CF_user ke [0.1, 1.0]
- CF 2.0 → di-clamp ke 1.0
- CF -0.5 → di-clamp ke 0.1
- Hasil diagnosis valid dan tidak error
- Tidak ada crash atau unexpected behavior

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-24: SEO & Meta Tags Check

### Tujuan
Verifikasi SEO elements ada

### Prasyarat
- Browser terbuka

### Steps
1. Buka `http://localhost:5000`
2. Buka DevTools → Elements/Inspector
3. Cek `<head>` section
4. Verifikasi meta tags:
   - `<meta charset="UTF-8">`
   - `<meta name="viewport">`
   - `<meta name="description">`
5. Cek `<title>` tag

### Expected Result
- Meta charset UTF-8 exists
- Meta viewport exists dengan content "width=device-width, initial-scale=1.0"
- Meta description exists dengan konten: "NetMedix - Sistem Pakar Diagnosis Masalah Jaringan Komputer berbasis Certainty Factor..."
- Title tag: "NetMedix — Diagnosis Jaringan" (atau sesuai halaman)
- Lighthouse SEO score: 100 ✅

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## TEST-25: Browser Compatibility Check

### Tujuan
Verifikasi aplikasi berfungsi di browser berbeda

### Prasyarat
- Akses ke multiple browser (Chrome, Firefox, Safari, Edge)

### Steps
1. Test di Google Chrome (latest)
2. Test di Mozilla Firefox (latest)
3. Test di Microsoft Edge (latest)
4. (Kalau bisa) Test di Safari (macOS/iOS)
5. Untuk setiap browser:
   - Buka home page
   - Lakukan diagnosis sederhana
   - Cek riwayat
   - Cek responsive layout

### Expected Result
- Semua browser menampilkan layout sama/tolerable
- JavaScript berfungsi (modal, navigation)
- CSS renders dengan benar (Tailwind CDN)
- Tidak ada browser-specific warning/error
- Core functionality works di semua browser

### Actual Result
- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes
---

## Summary Checklist

### Core Functionality (MUST PASS)
- [ ] TEST-01: Setup & Environment Check
- [ ] TEST-02: Halaman Home (Index Page)
- [ ] TEST-03: Halaman Diagnosis — Step 1 (Pilih Gejala)
- [ ] TEST-04: Tutorial Gejala (Modal Info Link)
- [ ] TEST-05: Halaman Diagnosis — Step 2 (Input CF User)
- [ ] TEST-06: Halaman Hasil Diagnosis (Result Page)
- [ ] TEST-07: Skenario Diagnosis — P02 (Internet Putus)
- [ ] TEST-08: Skenario Diagnosis — P05 (DHCP Failure)
- [ ] TEST-09: Skenario Edge Case — < 2 Gejala
- [ ] TEST-10: Skenario Edge Case — 0 Gejala
- [ ] TEST-11: Halaman Riwayat Diagnosis

### User Experience (SHOULD PASS)
- [ ] TEST-12: Halaman Admin — Login
- [ ] TEST-13: Halaman Admin — CRUD Rules (Optional)
- [ ] TEST-14: Halaman Tentang (About)
- [ ] TEST-15: Responsive Design — Mobile (375px)
- [ ] TEST-16: Accessibility Check (Keyboard Navigation)
- [ ] TEST-17: Color Contrast Check
- [ ] TEST-18: Performance Check — Load Time

### Error Handling & Edge Cases (NICE TO HAVE)
- [ ] TEST-19: Error Handling — 404 Page
- [ ] TEST-20: Error Handling — Tutorial Orphan Symptoms
- [ ] TEST-21: Database Check — History Persistence
- [ ] TEST-22: Cross-Cutting Symptoms Test
- [ ] TEST-23: CF Range Validation
- [ ] TEST-24: SEO & Meta Tags Check
- [ ] TEST-25: Browser Compatibility Check

---

## Pass/Fail Criteria

### Ready for Deployment
- **Semua Core Functionality tests PASS** (11/11)
- **Minimal 80% User Experience tests PASS** (≥5/7)
- **Tidak ada FAIL di Core Functionality**

### Need Fix Before Deployment
- Ada FAIL di Core Functionality
- < 80% User Experience tests PASS

### Blocker
- Ada BLOCKED test di Core Functionality
- Server tidak bisa start
- Database error
- Critical bug di result calculation

---

## Notes Tambahan

Gunakan section ini untuk mencatat temuan penting, bug, atau improvisasi selama testing:

```
[BUG FINDING]
Date:
Test ID:
Description:
Severity: [P0/P1/P2/P3]
Steps to reproduce:

[IMPROVEMENT IDEA]
Date:
Test ID:
Description:
Priority: [High/Medium/Low]

[GENERAL NOTES]
-
-
-
```

---

*Document created: 2026-07-16 | Version: 1.0 | Status: Ready for Manual Testing*
