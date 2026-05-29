# MoM Notetaker

Sistem otomatisasi notulen rapat (*Minutes of Meeting*) berbasis kecerdasan buatan (AI) menggunakan **FastAPI**, **Groq LLM (Llama 3)**, **n8n Automation**, dan **WhatsApp Gateway API (Baileys)**. Seluruh ekosistem ini sudah dikemas penuh ke dalam **Docker Compose** agar portabel dan siap dijalankan di laptop mana pun dengan instan.

---

##  Fitur Utama

- **AI-Powered Summarization:** Ekstraksi otomatis poin rapat menggunakan Llama 3 via Groq API.
- **Audio Transcription Support:** Transkripsi file rekaman suara menjadi teks mentah secara otomatis.
- **Full Docker Stack:** Sekali ketik, seluruh service (FastAPI + n8n + WhatsApp API) langsung menyala bersamaan.
- **Ultra-Fast Dependencies Management:** Sinkronisasi library Python otomatis menggunakan paket manager `uv` yang super cepat di dalam Docker.
- **Dual-Channel Delivery:** Hasil Minutes of Meeting (MoM) otomatis dikirimkan ke **Email (Gmail)** dan **WhatsApp** (Personal Chat maupun WhatsApp Group).

---

##  Struktur Project (Final)

Aplikasi ini memiliki susunan folder portabel sebagai berikut:

```bash
meeting-summary/
├── app/                        # Script utama backend FastAPI
│   ├── routers/                # Endpoint router (summarize.py)
│   ├── schemas/                # Validasi skema Pydantic (mom_schema.py)
│   ├── services/               # Core AI (pipeline, chunking, transcription)
│   └── utils/                  # Utility helper & Logger internal
│   └── app.py                  # Entrypoint inisialisasi FastAPI
├── auth_info_baileys/          # FOLDER KRUSIAL: Menyimpan token auto-login WhatsApp
├── input/                      # Tempat penyimpanan sementara file audio masuk
├── outputs/                    # Tempat penyimpanan file hasil transkripsi/notulen
├── .env                        # File konfigurasi API Key dan model LLM
├── docker-compose.yml          # Jantung orkestrasi Full-Stack Docker
├── Meeting_Notetaker.json      # Backup cetak biru workflow n8n
├── main.py                     # Script runner aplikasi
├── pyproject.toml              # Kunci manifes manajemen library oleh UV
├── uv.lock                     # Lockfile UV untuk stabilitas versi library
└── README.md                   # Dokumentasi panduan ini
```

## Panduan Menjalankan Sistem 
Ikuti 3 langkah mudah ini untuk memindahkan dan menyalakan project di laptop lain:

### Langkah 1: Siapkan File Environment (.env)
Pastikan kamu sudah membuat file bernama .env di folder utama project dan isi dengan API Key Groq kamu:


```bash

GROQ_API_KEY=gsk_your_real_api_key_here
LLM_MODEL=llama-3.1-8b-instant
WHISPER_MODEL=base

CHUNK_SIZE=3000
CHUNK_OVERLAP=200
```

### Langkah 2: Nyalakan Semua Service via Docker
Buka PowerShell atau CMD, masuk ke dalam folder meeting-summary, lalu jalankan perintah sakti ini:

```powersheel
docker compose up -d
```
*Catatan Penting Penggunaan Pertama*:

- Saat pertama kali dijalankan di laptop baru, Docker akan otomatis mendownload library Python menggunakan uv sync di latar belakang selama kurang lebih 1-2 menit.

- Berkat sistem uv-cache yang tertanam pada docker-compose, untuk penyalaan berikutnya (docker compose up atau down) sistem akan langsung aktif instan dalam waktu 2 detik tanpa download ulang.

### Langkah 3: Import Workflow ke n8n (Hanya Sekali di Awal)
Buka dashboard otomasi n8n di browser: http://localhost:5678

- Daftarkan akun admin baru jika diminta (bebas isi email & password).

- Di dalam lembar kerja kosong, klik tombol titik tiga (⋮) di pojok kanan atas layar.

- Pilih Import from File, lalu arahkan ke file cadangan Meeting_Notetaker.json yang ada di folder project kamu.

Aktifkan workflow tersebut (geser sakelar ke posisi Active di pojok kanan atas).

#### Panduan Integrasi WhatsApp & Email (Wajib di Awal)

Agar fitur pengiriman otomatis (Dual-Channel Delivery) ke WhatsApp dan Email berjalan dengan lancar, kamu wajib melakukan inisialisasi dua gerbang komunikasi ini saat pertama kali setup:

### 1. Aktivasi & Koneksi WhatsApp API (Baileys)
Service `wa-api` berjalan secara mandiri di port `3000`. Agar sistem bisa mengirimkan chat atas nama nomor WhatsApp kamu, ikuti trik sinkronisasi ini:

1. Pastikan seluruh container Docker sudah menyala (`docker compose up -d`).
2. Buka aplikasi **Docker Desktop** di laptop kamu.
3. Klik pada container bernama **`wa-api`**, lalu masuk ke tab **Logs**.
4. Di terminal log tersebut, kamu akan melihat sebuah **QR Code** berukuran besar yang dicetak oleh sistem Baileys.
5. Ambil HP kamu, buka **WhatsApp** -> ketuk menu **Perangkat Tertaut (Linked Devices)** -> klik **Tautkan Perangkat**, lalu arahkan kamera HP untuk **Scan QR Code** yang ada di log Docker tersebut.
6. Begitu sukses, log Docker akan memunculkan tulisan `[WA-API] Connection Open / Logged In`. 
7. *Keunggulan Sistem:* Token login akan otomatis terkunci di dalam folder `./auth_info_baileys` di laptopmu. Jadi, meskipun Docker kamu matikan atau laptop kamu restart, WhatsApp akan **tetap otomatis login** selamanya tanpa perlu scan ulang!

### 2. Konfigurasi Pengiriman Email via Google (GCP / App Password)
Workflow n8n membutuhkan akses aman ke server SMTP Google agar bisa mengirim notifikasi notulen rapat via Gmail kamu. Karena Google melarang penggunaan password utama demi keamanan, kita wajib menggunakan **App Password**:

1. Buka pengaturan akun Google kamu di [Google Account Security](https://myaccount.google.com/security).
2. Pastikan Akun Google kamu sudah mengaktifkan **Verifikasi 2 Langkah (2-Step Verification)**.
3. Ketik kata kunci **"Sandi Aplikasi"** atau **"App Passwords"** pada kolom pencarian di bagian atas akun Google kamu.
4. Buat sandi aplikasi baru, beri nama (contoh: `n8n MoM Notetaker`), lalu klik **Buat (Create)**.
5. Google akan memunculkan **16 digit kode rahasia** (tanpa spasi). Salin kode tersebut!
6. Buka dashboard **n8n** (`http://localhost:5678`), masuk ke node **Gmail / SMTP Email**, lalu masukkan kredensial berikut:
   - **User:** Email Gmail kamu (`emailkamu@gmail.com`)
   - **Password:** Masukkan *16 digit kode Sandi Aplikasi* yang kamu salin tadi (bukan password email utama kamu).
   - **SSL/TLS:** Enabled (Port 465) atau STARTTLS (Port 587).
7. Klik **Test Connection** di n8n untuk memastikan email siap mengirim rangkuman rapat secara otomatis.

## Endpoint Developer & Swagger UI
Jika kamu ingin menguji performa backend AI secara manual atau membaca spesifikasi skema datanya, kamu bisa mengakses Dokumentasi API Interaktif (Swagger UI) pada alamat berikut:

http://localhost:8000/docs

POST /summarize: Endpoint utama yang menerima file .mp3, .wav, .txt, .srt, atau .vtt untuk dianalisis oleh AI pipeline menjadi struktur JSON MoM yang rapi.
