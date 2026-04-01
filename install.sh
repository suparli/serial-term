#!/bin/bash

# ========================================================
# Bash Installer untuk Linux & macOS
# Ganti YOUR_USERNAME/YOUR_REPO_NAME dengan nama repo Anda!
# ========================================================

REPO="suparli/serial-term"
APP_NAME="serial-term"
INSTALL_DIR="/usr/local/bin"

echo "Mendeteksi Sistem Operasi..."
OS="$(uname -s)"
case "${OS}" in
    Linux*)     FILE_NAME="serial-term-linux";;
    Darwin*)    FILE_NAME="serial-term-macos";;
    *)          echo "Sistem Operasi tidak didukung: ${OS}" && exit 1;;
esac

echo "Mengambil URL Rilis Terbaru dari GitHub..."
DOWNLOAD_URL=$(curl -s https://api.github.com/repos/${REPO}/releases/latest \
| grep "browser_download_url.*${FILE_NAME}" \
| cut -d : -f 2,3 \
| tr -d \")

if [ -z "$DOWNLOAD_URL" ]; then
    echo "Gagal menemukan rilis terbaru untuk sistem operasi Anda."
    echo "Pastikan REPO di script ini benar dan rilis sudah dibuat di GitHub."
    exit 1
fi

echo "Mengunduh ${APP_NAME}..."
curl -L -o /tmp/${APP_NAME} ${DOWNLOAD_URL}

echo "Memasang ${APP_NAME} ke ${INSTALL_DIR} (Mungkin butuh password sudo)..."
sudo mv /tmp/${APP_NAME} ${INSTALL_DIR}/${APP_NAME}
sudo chmod +x ${INSTALL_DIR}/${APP_NAME}

echo "Selesai! Anda sekarang dapat menjalankan perintah: ${APP_NAME}"
