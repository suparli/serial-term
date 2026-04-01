# ==========================================================
# Manual Build Script untuk Windows (PowerShell)
# Jalankan ini jika Anda ingin build sendiri di komputer Anda
# ==========================================================

Write-Host "Memulai Proses Build Manual menggunakan PyInstaller..." -ForegroundColor Cyan

# Pastikan pip dan pyinstaller terinstal
python -m pip install --upgrade pip
pip install pyinstaller
pip install -r requirements.txt

# Menjalankan PyInstaller (satu file executable)
pyinstaller --onefile --name serial-term main.py

Write-Host "Build Selesai!" -ForegroundColor Green
Write-Host "File executable Anda bisa ditemukan di dalam folder 'dist\serial-term.exe'" -ForegroundColor Yellow
Write-Host "Untuk menguji aplikasinya, jalankan perintah: .\dist\serial-term.exe"
