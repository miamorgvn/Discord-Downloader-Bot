# Universal Discord Downloader Bot

Bot Discord serbaguna berbasis Python yang dirancang untuk mendeteksi, mengambil, dan mengunduh media (video/foto) secara otomatis dari berbagai platform media sosial utama langsung ke dalam channel obrolan Discord.

## 🚀 Fitur Utama
- **Multi-Platform Support**: Mampu mengunduh konten video dan media dari berbagai platform populer (Instagram, TikTok, YouTube Shorts, Twitter/X, dll).
- **Universal Link Parser**: Sistem pintar yang otomatis mendeteksi tautan media di dalam obrolan tanpa perlu perintah manual.
- **Session & Cookie Management**: Menggunakan manajemen berkas sesi lokal untuk melewati batas enkripsi platform dan mengunduh konten secara privat dengan aman.
- **Secure Environment**: Proteksi kredensial sensitif menggunakan enkapsulasi variabel lingkungan (`.env`).

## 🛠️ Teknologi yang Digunakan
- **Bahasa Pemrograman**: Python
- **Library Utama**: Discord.py, Python-dotenv, Requests/YTDL-Core
- **Version Control**: Git & GitHub

## ⚙️ Panduan Instalasi di Termux

Jika Anda ingin mencoba menjalankan bot ini di Termux, ikuti langkah-langkah berikut:

### 1. Install Alat Dasar
Buka Termux Anda, lalu jalankan perintah berikut untuk menginstal Python dan Git:
```bash
pkg update && pkg upgrade -y
pkg install python git -y
```

### 2. Kloning Repositori
Unduh kodingan bot ini dari GitHub ke Termux Anda:
```bash
git clone https://github.com
cd discord-downloader
```

### 3. Install Library Pendukung
Install semua library Python yang dibutuhkan bot ini sekaligus:
```bash
pip install -r requirements.txt
```

### 4. Setel Token Akses
Buat file rahasia `.env` untuk menyimpan token bot Discord Anda:
```bash
nano .env
```
Masukkan teks berikut di dalamnya (ganti dengan token bot Anda):
```text
DISCORD_TOKEN=MASUKKAN_TOKEN_DISCORD_ANDA
```
Simpan dengan menekan **CTRL + X**, lalu **Y**, lalu **Enter**.

### 5. Jalankan Bot
Sekarang bot siap dijalankan dengan mengetik perintah:
```bash
python bot.py
```
