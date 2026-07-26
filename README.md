# NetMedix

**Sistem Pakar Diagnosis Masalah Jaringan Komputer** menggunakan metode **Pure Certainty Factor** dengan **CF_pakar berbasis riset multi-source**.

Proyek UAS mata kuliah Sistem Cerdas — Semester 4 Informatika.

---

## Tentang

NetMedix adalah aplikasi web yang membantu pengguna mengidentifikasi masalah jaringan komputer berdasarkan gejala-gejala yang dialami. Pengguna memilih gejala, menentukan tingkat keyakinan, dan sistem menghitung diagnosis menggunakan metode **Pure Certainty Factor (CF)** dengan nilai **CF_pakar** yang diturunkan dari riset literatur multi-source.

### Fitur Utama

- **Diagnosis 3 Langkah** — pilih gejala, tentukan keyakinan (5 level), lihat hasil lengkap
- **15 masalah jaringan** dalam 7 kategori (Konektivitas, DNS, DHCP, WiFi, Performa, Keamanan, Hardware)
- **40 gejala** dengan tutorial inline — info gejala + panduan verifikasi
- **15 aturan IF-THEN** dengan **CF_pakar riset-based** (bukan MB/MD arbitrer)
- **Filter ≥ 2 gejala relevan** — diagnosis lebih akurat meski gejala user tidak lengkap
- **Detail perhitungan CF** — step-by-step evidence (CF_pakar × CF_user) dan kombinasi
- **Kesimpulan naratif** — ringkasan masalah utama + alternatif dalam bahasa natural
- **Tutorial per gejala** — halaman dedicated dengan definisi, cara verifikasi, interpretasi
- **Riwayat diagnosis** — tersimpan di SQLite, bisa dilihat dan dihapus
- **Admin Panel** — CRUD knowledge base (masalah, gejala, aturan) tanpa edit JSON manual
- **Responsif** — desktop, tablet, mobile

---

## Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Backend | Python 3.10+ / Flask 3.x |
| Frontend CSS | Tailwind CSS 3.x (CDN) |
| Frontend JS | Vanilla JavaScript |
| Font | Inter (Google Fonts) |
| Icons | Lucide Icons (CDN) |
| Template | Jinja2 (bundled with Flask) |
| Knowledge Base | JSON files |
| Database | SQLite 3 (Python stdlib) |

Zero build step. Semua dependensi frontend via CDN.

---

## Instalasi & Menjalankan

### Prasyarat

- Python 3.10 atau lebih baru

### Langkah

```bash
# 1. Clone atau masuk ke direktori project
cd NetMedix

# 2. Buat virtual environment (jika belum ada)
python3 -m venv venv

# 3. Aktifkan venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 4. Install dependensi
pip install flask

# 5. Jalankan aplikasi
python app.py
```

Buka browser ke **http://localhost:5000**

---

## Deployment ke Server

### Opsi 1: Docker Compose (Recommended)

Docker Compose adalah cara termudah untuk deployment ke server.

#### A. Siapkan File untuk Deployment

**Files yang WAJIB diikutkan:**

```bash
# Core Application
app.py
requirements.txt

# Inference Engine
inference/__init__.py
inference/engine.py
inference/knowledge_base.py

# Knowledge Base (JSON files)
data/problems.json
data/symptoms.json
data/rules.json

# Templates (HTML files)
templates/*.html
templates/admin/*.html

# Static Assets
static/js/app.js
static/css/ (jika ada custom CSS selain Tailwind CDN)

# Docker Files
Dockerfile                    # Production image
Dockerfile.dev                # Development image (opsional)
docker-compose.yml            # Development compose
docker-compose.prod.yml       # Production compose (REQUIRED)
.dockerignore

# Configuration
.env.example                  # Template environment variables
nginx/nginx.conf              # Nginx configuration
```

**Files yang TIDAK PERLU diikutkan:**

```bash
# Git files
.git/
.gitignore

# Python artifacts
__pycache__/
*.py[cod]
*.pyc
*.pyo
.venv/
venv/
env/

# Database (akan dibuat otomatis di server)
database/*.db
database/*.db-journal

# Logs
*.log
flask.log

# IDE files
.vscode/
.idea/
*.swp

# Documentation (opsional)
*.md
docs-NetMedix/

# Docker development files (opsional)
Dockerfile.dev
docker-compose.yml
```

#### B. Buat Deployment Zip

**Cara 1: Menggunakan Script (Recommended)**

```bash
# Di local machine, di root project NetMedix
cd /path/to/NetMedix

# Buat folder temporary untuk deployment
mkdir -p netmedix-deploy

# Copy essential files
cp app.py requirements.txt netmedix-deploy/
cp -r inference/ netmedix-deploy/
cp -r data/ netmedix-deploy/
cp -r templates/ netmedix-deploy/
cp -r static/ netmedix-deploy/
cp Dockerfile docker-compose.prod.yml .dockerignore .env.example netmedix-deploy/
mkdir -p netmedix-deploy/nginx
cp nginx/nginx.conf netmedix-deploy/nginx/

# Buat zip
zip -r netmedix-v2.0.0-deploy.zip netmedix-deploy/

# Cleanup temporary folder
rm -rf netmedix-deploy/
```

**Cara 2: Manual Selection**

Select dan zip files berikut:
- `app.py`
- `requirements.txt`
- Folder `inference/`
- Folder `data/` (hanya .json files)
- Folder `templates/`
- Folder `static/`
- `Dockerfile`
- `docker-compose.prod.yml`
- `.dockerignore`
- `.env.example`
- Folder `nginx/` dengan `nginx.conf`

#### C. Upload ke Server

```bash
# Upload zip ke server (ganti user@host dengan server Anda)
scp netmedix-v2.0.0-deploy.zip user@yourserver.com:/home/user/

# Atau menggunakan SFTP/FTP client
# - FileZilla
# - WinSCP
# - Cyberduck
```

#### D. Setup di Server

```bash
# 1. Login ke server
ssh user@yourserver.com

# 2. Extract zip
cd ~
unzip netmedix-v2.0.0-deploy.zip
cd netmedix-deploy

# 3. Setup environment variables
cp .env.example .env
nano .env  # Edit SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD

# 4. (Opsional) Setup SSL certificates
mkdir -p nginx/ssl
# Letakkan cert.pem dan key.pem di nginx/ssl/

# 5. Build dan start containers
docker compose -f docker-compose.prod.yml up -d --build

# 6. Cek status
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f
```

**Aplikasi akan berjalan di:**
- HTTP: `http://your-server-ip`
- HTTPS: `https://your-server-ip` (jika SSL configured)

#### E. Management Commands

```bash
# View logs
docker compose -f docker-compose.prod.yml logs -f

# Restart containers
docker compose -f docker-compose.prod.yml restart

# Stop containers
docker compose -f docker-compose.prod.yml down

# Update aplikasi (setelah upload zip baru)
docker compose -f docker-compose.prod.yml down
unzip -o netmedix-v2.0.0-deploy.zip
docker compose -f docker-compose.prod.yml up -d --build

# Backup database
docker cp netmedix-app-prod:/app/database/history.db ./backups/
```

---

### Opsi 2: Traditional Deployment (Tanpa Docker)

Jika server tidak mendukung Docker.

#### Prasyarat di Server

```bash
# Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip nginx

# Install Python dependencies
pip3 install flask gunicorn
```

#### Setup Application

```bash
# 1. Upload dan extract file sama seperti di atas
unzip netmedix-v2.0.0-deploy.zip
cd netmedix-deploy

# 2. Setup environment
cp .env.example .env
nano .env

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Run dengan Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 app:app
```

#### Nginx Reverse Proxy

```bash
# Edit nginx config
sudo nano /etc/nginx/sites-available/netmedix

# Tambahkan konfigurasi:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.0:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/netmedix-deploy/static/;
        expires 30d;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/netmedix /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| Container tidak start | `docker compose logs netmedix-app` |
| Permission denied | `chmod +x database/` atau check file permissions |
| Port 80 already in use | Stop apache2: `sudo systemctl stop apache2` |
| Database locked | Restart container: `docker compose restart netmedix-app` |
| Nginx 502 Bad Gateway | Check jika app container running: `docker compose ps` |

---

### Security Checklist

Sebelum production:

- [ ] `.env` file ada di `.gitignore`
- [ ] Default admin password diubah
- [ ] SSL certificates configured (untuk HTTPS)
- [ ] Firewall configured: `sudo ufw allow 80/tcp && sudo ufw allow 443/tcp`
- [ ] Regular backup setup untuk database
- [ ] Monitor disk space dan logs

---

## Struktur Proyek

```
NetMedix/
├── app.py                    # Flask entry point (routes, DB, auth)
├── inference/
│   ├── __init__.py
│   ├── engine.py             # Forward Chaining + Certainty Factor
│   └── knowledge_base.py     # JSON loader & query methods
├── data/
│   ├── problems.json          # 15 masalah jaringan (P01-P15)
│   ├── symptoms.json          # 40 gejala (G01-G40)
│   └── rules.json             # 15 aturan IF-THEN + MB/MD (R01-R15)
├── templates/
│   ├── base.html              # Base layout
│   ├── index.html             # Landing page
│   ├── diagnose.html          # Step 1 — Pilih Gejala
│   ├── diagnose_step2.html    # Step 2 — Tingkat Keyakinan
│   ├── result.html            # Step 3 — Hasil Diagnosis
│   ├── about.html             # Tentang sistem
│   ├── history.html           # Riwayat diagnosis
│   ├── 404.html / 500.html    # Error pages
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── problems.html      # CRUD masalah
│       ├── symptoms.html      # CRUD gejala
│       └── rules.html         # CRUD aturan
├── static/js/app.js           # Client-side JS
├── database/                  # SQLite (auto-created)
└── venv/
```

---

## Metode

### Pure Certainty Factor (CF)

NetMedix v2.0.0 menggunakan metode **Pure Certainty Factor** tanpa MB/MD. Tingkat keyakinan pakar (CF_pakar) diturunkan langsung dari riset literatur multi-source (Microsoft Learn, Cisco, CompTIA, dll).

### Certainty Factor (CF)

Mengukur tingkat keyakinan terhadap diagnosis menggunakan dua rumus:

**1. CF Evidence** — gabungan keyakinan pakar dan user:
```
CF_evidence = CF_user × CF_pakar
```

**2. CF Combine** — kombinasi beberapa evidence:
```
CF_combine = CF₁ + CF₂ × (1 - CF₁)
```

### Filter Diagnosis

Sistem menggunakan filter "≥ 2 gejala relevan" — diagnosis hanya muncul jika minimal 2 gejala dari aturan tersebut dipilih user. Ini meningkatkan akurasi dan mengurangi false positive.

### Contoh Perhitungan

Diagnosis "Koneksi Internet Terputus" (P02) dengan input G02=1.0, G03=1.0, G28=0.8:

| Gejala | CF_pakar | CF_user | CF_evidence |
|--------|----------|---------|-------------|
| G02    | 0.95     | 1.00    | 0.950       |
| G03    | 0.90     | 1.00    | 0.900       |
| G28    | 0.80     | 0.80    | 0.640       |

```
Step 1: CF_evidence(G02) = 1.00 × 0.95 = 0.950
Step 2: combine(0.950, 0.900) = 0.950 + 0.900 × 0.050 = 0.995
Step 3: combine(0.995, 0.640) = 0.995 + 0.640 × 0.005 = 0.998
```

**Hasil: P02 — Koneksi Internet Terputus, CF = 99.8% (Sangat Yakin)**

---

## Knowledge Base

### Masalah Jaringan (15)

| Kategori | Masalah |
|----------|---------|
| Konektivitas Dasar | P01 Tidak Ada Koneksi, P02 Internet Terputus |
| DNS | P03 Resolution Failure, P04 Cache Poisoning |
| DHCP & IP Config | P05 DHCP Failure, P06 IP Conflict, P07 Subnet/Gateway Salah |
| WiFi | P08 Tidak Bisa Connect, P09 Signal Lemah |
| Performa | P10 Jaringan Lambat, P11 Packet Loss, P12 Latensi Tinggi |
| Keamanan | P13 Firewall Memblokir |
| Hardware | P14 Kerusakan Kabel, P15 Kerusakan Router/Switch |

### Gejala (40)

Tersebar di 7 kategori: Konektivitas (11), DNS (4), DHCP & IP Config (6), WiFi (4), Performa (5), Keamanan (4), Hardware (6).

---

## Halaman

| Route | Deskripsi |
|-------|-----------|
| `/` | Landing page — hero, cara kerja, kategori, statistik |
| `/diagnose` | Step 1 — pilih gejala (tab per kategori) dengan info button ⓘ |
| `/diagnose/step2` | Step 2 — tentukan tingkat keyakinan (5 level: 0.1-1.0) |
| `/diagnose/process` | Process inference — jalankan engine diagnosis |
| `/result/<session_id>` | Step 3 — hasil diagnosis lengkap + kesimpulan naratif + trace perhitungan |
| `/tutorial/<code>` | Tutorial gejala — definisi, cara verifikasi, interpretasi, penyebab umum |
| `/history` | Riwayat semua diagnosis (dengan lazy render v1/v2) |
| `/about` | Penjelasan metode Pure Certainty Factor |
| `/admin/login` | Login admin (default: admin / admin123) |
| `/admin` | Dashboard admin |
| `/admin/problems` | CRUD masalah jaringan |
| `/admin/symptoms` | CRUD gejala (dengan field tutorial v2) |
| `/admin/rules` | CRUD aturan IF-THEN (dengan CF_pakar, evidence, sources v2) |

---

## Admin Panel

Login default:

```
Username: admin
Password: admin123
```

Melalui admin panel, knowledge base dapat dikelola tanpa mengedit file JSON secara manual. Perubahan langsung berpengaruh ke diagnosis.

---

## Dokumentasi Tambahan

| File | Isi |
|------|-----|
| `SRS.md` | Software Requirements Specification |
| `PRD.md` | Product Requirements Document |
| `DESIGN.md` | Design system reference |
| `TODO.md` | Step-by-step task tracker (all done) |
| `VERSION-CONTROL.md` | Version history & changelog |

---

## Changelog v2.0.0

### Breaking Changes dari v1.0.0

| Area | v1.0.0 | v2.0.0 |
|------|--------|--------|
| **Metode** | Forward Chaining AND-strict + CF (MB-MD) | Pure CF dengan filter ≥ 2 gejala |
| **Formula CF** | 3 rumus (CF_rule, CF_evidence, CF_combine) | 2 rumus (CF_evidence, CF_combine) |
| **CF Pakar** | Diderivasi dari MB − MD | Langsung dari riset multi-source |
| **rules.json** | `{mb, md}` per gejala | `{cf_pakar, evidence}` per gejala + `sources` per rule |
| **symptoms.json** | `{code, name, category}` | + `{short_desc, how_to_check, tutorial}` |
| **Range CF_user** | [-1, 1] (9 level) | [0.1, 1.0] (5 level) |
| **UI Input CF** | Free input / select dropdown | Radio button 5 level |
| **Output Diagnosis** | Top-3 kandidat | Semua kandidat yang lolos filter |
| **Tutorial Gejala** | Tidak ada | Tooltip ⓘ + halaman /tutorial/<code> |
| **Kesimpulan** | Tidak ada | Narasi natural di atas hasil |
| **History SQLite** | v1 schema | Lazy render (deteksi v1 vs v2) |

### Fitur Baru v2.0.0

- **Tutorial Inline per Gejala** — setiap gejala punya info button dengan panduan verifikasi
- **Halaman Tutorial Dedicated** — `/tutorial/<code>` dengan definisi, steps, interpretasi, causes
- **CF_pakar Riset-Based** — semua nilai pakar diturunkan dari ≥2 sumber literatur
- **Kesimpulan Naratif** — ringkasan masalah utama + alternatif dalam bahasa natural
- **Filter Lebih Cerdas** — hanya muncul jika ≥2 gejala relevan (reduksi false positive)
- **Evidence Justifikasi** — setiap CF_pakar punya catatan justifikasi di trace
- **Label Persentase** — semua hasil ada persentase × 100 + label (Sangat Yakin, dll)

### Migration Notes untuk Pengguna v1.0.0

**Jika Anda memiliki histori diagnosis lama (v1):**
- Histori lama otomatis terdeteksi dan di-render dengan fallback "diagnosa v1"
- Data lama tetap bisa dilihat, tapi tidak akan menampilkan field baru (percentage, label)
- Tidak perlu migrasi manual — sistem lazy render otomatis

**Untuk developer/admin:**
- Backup `rules.json` dan `symptoms.json` v1 sudah ada di `.v1.0.0.json.bak`
- **Admin panel belum diupdate untuk schema v2** — untuk sementara edit JSON langsung untuk perubahan KB
- Histori SQLite structure tetap sama — hanya ada lazy render untuk field baru
- Semua fitur diagnosis v2.0.0 sudah fully functional tanpa admin panel update

---

## Referensi

- Kusumadewi, S. (2003). *Artificial Intelligence (Teknik Pengembangan Komputasi)*. Graha Ilmu.
- Negnevitsky, M. (2024). *Artificial Intelligence: A Guide to Intelligent Systems* (4th ed.). Pearson.
- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Shortliffe, E.H. & Buchanan, B.G. (1975). "A model of inexact reasoning in medicine." *Mathematical Biosciences*.
- CompTIA Network+ (N10-008) — referensi domain troubleshooting jaringan.

---

*NetMedix v2.0.0 — Proyek UAS Sistem Cerdas 2026*

**Documentation Version:** 2026-07-16
