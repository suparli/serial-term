# 🔌 Serial-Term

![Build Status](https://github.com/suparli/serial-term/actions/workflows/release.yml/badge.svg)
![OS Supported](https://img.shields.io/badge/OS-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)

Aplikasi Terminal (CLI) interaktif dan lintas platform (*Cross-Platform*) untuk keperluan komunikasi Serial & Bluetooth. Dibuat dengan antarmuka Command Line yang modern, cantik, dan mudah digunakan langsung dari terminal Anda!

---

## ✨ Fitur Utama
- **Cross-Platform:** Berjalan dengan mulus di Windows, Linux, dan macOS.
- **Single Executable:** Pengguna tidak perlu menginstal Python atau pustaka pendukung lainnya. Cukup unduh dan jalankan!
- **Antarmuka Modern:** Dibangun menggunakan teknologi *Textual / Rich* untuk menghadirkan UI terminal yang responsif dan interaktif.
- **Instalasi Instan:** Tersedia skrip installer otomatis untuk Bash dan PowerShell.

---

## 🚀 Cara Instalasi

Anda dapat menginstal aplikasi ini hanya dengan **satu baris perintah** di terminal Anda.

### 🐧 Linux & 🍏 macOS (Bash)
Buka terminal favorit Anda dan jalankan perintah ini:
```bash
curl -sL https://raw.githubusercontent.com/suparli/serial-term/main/install.sh | bash
```

### 🪟 Windows (PowerShell)
Buka aplikasi **PowerShell** dan jalankan perintah ini:
```powershell
Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/suparli/serial-term/main/install.ps1')
```
*(Catatan: Setelah instalasi selesai, Anda mungkin perlu menutup dan membuka kembali PowerShell Anda).*

---

## 💻 Penggunaan

Setelah instalasi selesai, Anda dapat membuka aplikasi ini dari direktori mana saja di komputer Anda (CMD, PowerShell, Bash, atau Zsh) cukup dengan mengetik:

```bash
serial-term
```

---

## 🛠️ Build Manual & Pengembangan (Untuk Developer)

Jika Anda ingin ikut mengembangkan aplikasi ini atau melakukan kompilasi mandiri di komputer Anda:

1. Clone repository ini: 
   ```bash
   git clone https://github.com/suparli/serial-term.git
   cd serial-term
   ```
2. Buat *Virtual Environment* (Disarankan):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   .\venv\Scripts\activate   # Untuk Windows
   ```
3. Install semua dependencies: 
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan script Build:
   - **Windows:** Jalankan `.\build.ps1`
   - **Linux/Mac:** Gunakan perintah manual `pyinstaller --onefile --name serial-term main.py`

File *executable* hasil build akan tersedia di dalam folder `dist/`.

---

## 🤝 Kontribusi
Kami sangat menyambut kontribusi Anda! Silakan *fork* repository ini, buat branch fitur Anda, dan kirimkan *Pull Request*. Jika ada bug, jangan ragu untuk membuka *Issue*.
