# NetMedix - Catatan Gemini

## Analisis Project (v2.0.0)

NetMedix adalah aplikasi Sistem Pakar diagnosis medis berbasis web yang menggunakan metode **Certainty Factor (CF)** untuk menghitung tingkat keyakinan diagnosis berdasarkan gejala yang dipilih oleh pengguna.

### 1. Arsitektur & Teknologi Stack
- **Backend Framework**: Python Flask (`Flask==3.1.3`).
- **Database**: SQLite3 (`database/history.db`), database berbasis file lokal untuk mencatat sesi riwayat diagnosis.
- **Inference Engine**: Custom Python code (`inference/engine.py` & `inference/knowledge_base.py`) untuk implementasi Certainty Factor murni.
- **Knowledge Base**: Disimpan dalam format berkas JSON di folder `data/` (`problems.json`, `symptoms.json`, `rules.json`).
- **Frontend**: HTML5 (Jinja2 templates di `templates/`) dan Vanilla CSS / Javascript (`static/`).

### 2. Struktur Folder Utama
- `app.py`: Entry point aplikasi web, mendefinisikan routing Flask, autentikasi admin, sesi diagnosis, dan operasi CRUD database riwayat.
- `inference/`: Logika bisnis dari sistem pakar (perkalian CF user * pakar, kombinasi CF, dan penyaringan minimal 2 gejala relevan).
- `data/`: File data pengetahuan penyakit (problems), gejala (symptoms), dan relasi/aturan (rules).
- `database/`: Lokasi database SQLite `history.db`.
- `static/` & `templates/`: Berkas aset web dinamis/statis.
- `requirements.txt`: Dependensi Python (hanya membutuhkan `Flask`).

---

## Panduan Deployment di aaPanel

Aplikasi Flask seperti NetMedix **sangat bisa dan mudah** di-hosting di **aaPanel** menggunakan fitur bawaan **Python Group Project** (atau **Python Manager**).

### Langkah-langkah Hosting:

1. **Persiapan Server & aaPanel**:
   - Pastikan aaPanel sudah terinstal di server VPS Linux (Ubuntu/Debian/CentOS).
   - Pastikan Nginx terinstal melalui App Store aaPanel untuk bertindak sebagai Reverse Proxy.

2. **Instalasi Python Project Manager**:
   - Buka menu **App Store** di aaPanel.
   - Cari **"Python Group Project"** (atau **"Python Manager"**) lalu klik **Install**.

3. **Upload File Project**:
   - Buka menu **Files** di aaPanel.
   - Buat direktori baru di `/www/wwwroot/netmedix` (atau sesuaikan dengan nama domain Anda).
   - Unggah semua file project Anda ke direktori tersebut. Anda tidak perlu mengunggah folder `venv` lokal atau file cache `__pycache__` karena aaPanel akan membuat lingkungan virtual (`venv`) baru di server.

4. **Konfigurasi Project Python di aaPanel**:
   - Buka menu **Website** -> **Python Project** -> klik **Add Project**.
   - Isi form konfigurasi sebagai berikut:
     - **Project Path**: Pilih folder project `/www/wwwroot/netmedix`.
     - **Project Name**: `netmedix` (atau bebas).
     - **Run Path**: Pilih letak berkas utama, yaitu `/www/wwwroot/netmedix`.
     - **Startup File**: Pilih `app.py`.
     - **Python Version**: Pilih versi Python 3.x (aaPanel akan mendeteksi otomatis atau mengunduh versi Python yang diinginkan jika belum ada).
     - **Framework**: Pilih `Flask`.
     - **Run Command**: Biasanya otomatis (`gunicorn -w 4 -b 127.0.0.1:port app:app` atau disesuaikan).
     - **Port**: Tentukan port internal bebas (misal `5000` atau `8000`).
     - **Create Virtual Environment**: Centang (Ya) agar library terisolasi secara bersih.
     - **Install Requirements**: Centang (Ya) agar aaPanel menginstal otomatis package Flask dari `requirements.txt`.
   - Klik **Submit** untuk membuat project.

5. **Mapping Domain (Reverse Proxy)**:
   - Setelah project berhasil dijalankan, klik tombol **Mapping** di sebelah kanan nama project pada daftar Python Project.
   - Masukkan domain atau subdomain Anda (misal `netmedix.domainanda.com`).
   - aaPanel akan otomatis membuat konfigurasi reverse proxy Nginx yang mengarahkan trafik domain tersebut ke port internal Flask yang berjalan di Gunicorn.

6. **Konfigurasi Hak Akses Database (SQLite)**:
   - Karena SQLite3 menyimpan data ke dalam file lokal (`database/history.db`), pastikan user server (biasanya `www`) memiliki hak akses baca dan tulis (*read and write permission*) ke folder `database` dan file `history.db`.
   - Di menu **Files**, arahkan ke folder `/www/wwwroot/netmedix/database`.
   - Klik kanan pada folder `database`, pilih **Permission**, lalu atur permission menjadi `755` atau `777` dengan owner `www:www` (tergantung konfigurasi user jalannya aplikasi web). Hal ini penting untuk menghindari error `sqlite3.OperationalError: attempt to write a readonly database`.

7. **Konfigurasi Environment Variables (Opsional)**:
   - Jika Anda ingin meningkatkan keamanan, ubah variabel `SECRET_KEY`, `ADMIN_USERNAME`, dan `ADMIN_PASSWORD` menggunakan Environment Variables di server Anda atau buat file `.env` dan gunakan pustaka `python-dotenv`.
