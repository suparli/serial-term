# ========================================================
# PowerShell Installer untuk Windows
# Ganti YOUR_USERNAME/YOUR_REPO_NAME dengan nama repo Anda!
# ========================================================

$Repo = "suparli/serial-term"
$AppName = "serial-term"
$FileName = "serial-term.exe"
$InstallDir = "$env:LOCALAPPDATA\$AppName\bin"

Write-Host "Memeriksa Rilis Terbaru dari GitHub..."
$ApiUrl = "https://api.github.com/repos/$Repo/releases/latest"

try {
    $Release = Invoke-RestMethod -Uri $ApiUrl -ErrorAction Stop
} catch {
    Write-Error "Gagal mendapatkan rilis terbaru. Pastikan REPO di script sudah benar."
    exit
}

$Asset = $Release.assets | Where-Object { $_.name -eq $FileName }
if (-not $Asset) {
    Write-Error "File ${FileName} tidak ditemukan di rilis terbaru."
    exit
}

Write-Host "Mengunduh ${AppName}..."
$DownloadUrl = $Asset.browser_download_url
$TempFile = "$env:TEMP\$FileName"
Invoke-WebRequest -Uri $DownloadUrl -OutFile $TempFile

Write-Host "Memasang ${AppName}..."
if (-not (Test-Path -Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

Move-Item -Path $TempFile -Destination "$InstallDir\$FileName" -Force

Write-Host "Menambahkan ke Environment Variable PATH..."
$UserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($UserPath -notlike "*$InstallDir*") {
    $NewPath = "$UserPath;$InstallDir"
    [Environment]::SetEnvironmentVariable("PATH", $NewPath, "User")
    Write-Host "PATH berhasil ditambahkan. Silakan Buka Ulang Terminal (CMD/PowerShell) Anda." -ForegroundColor Green
} else {
    Write-Host "Direktori sudah ada di PATH." -ForegroundColor Yellow
}

Write-Host "Selesai! Buka ulang PowerShell Anda dan jalankan perintah: ${AppName}" -ForegroundColor Green
