# Rencana UI & Fitur Koneksi Lengkap

Berdasarkan permintaan tambahan Anda, saya telah menggabungkan rencana fitur parameter serial (Baudrate, dll) bersama dengan kontrol pertukaran data biner/hexadecimal murni (**HEX Send** & **HEX Receive**).

## User Review Required
Berikut adalah *blueprint* tata letak (*layout*) terminal Anda yang baru. Tolong pastikan ini sudah memenuhi semua kebutuhan *debugging* Anda sebelum saya mulai mengeksekusinya menjadi kode.

---

## 1. Tata Letak (Interface Layout) Baru
Mengingat cukup banyak menu dropdown (*Select*) dan Sakelar (*Checkbox*) yang harus Anda lihat sekaligus, saya mengajukan pemisahan bilah navigasi (Header) menjadi 2 baris agar tampilan tetap rapi, rapi, dan responsif.

```text
[ Baris 1 - Utama ]
[ Device_Target_Combo ] [ Connect ] [ Scan Devices ] Status: Disconnected

[ Baris 2 - Pengaturan Serial & Format ]
[ BaudRate ] [ DataBits ] [ Parity ] [ StopBits ] [ FlowCtrl ] 
(Sakelar/Checkbox): ☑ Hex Receive   ☑ Hex Send
```

## 2. Implementasi Fungsional

### A. Fitur Parser Format (Hex/ASCII)
Akan memanfaatkan file `ui/formatter.py` yang sebelumnya sudah di-stub:
- **`[ ] Hex Receive`**: Jika dicentang, ketika perangkat keras mengirim *stream* (misal byte: `0xDE 0xAD`), ia akan dicetak ke dalam RichLog secara harfiah `DE AD` tanpa perlu memaksakan *decoding UTF-8* yang menghasilkan teks sampah/karakter tak terbaca ().
- **`[ ] Hex Send`**: Jika dicentang, input teks di balok (command bar) bawah dengan format `FF 0A 1B` akan dikonversi menjadi *array byte* mentah `[255, 10, 27]` kemudian dikirim ke dalam TX *pyserial/bleak*, alih-alih dienkodekan ASCII/UTF-8.

### B. Parameter Lengkap Koneksi Serial (Pyserial)
Fungsi utama `serial_handler.py` akan dimodifikasi (*overloading*) untuk menerima `**kwargs` dari nilai yang ada di *Dropdown* baris kedua ketika tombol **Connect** (di baris pertama) ditekan.
Opsi Dropdown:
- **Baudrate:** `9600`, `19200`, `38400`, `57600`, `115200` (Default), `230400`
- **Data Bits:** `5`, `6`, `7`, `8` (Default)
- **Parity:** `None` (Default), `Even`, `Odd`, `Mark`, `Space`
- **Stop Bits:** `1` (Default), `1.5`, `2`
- **Flow Ctrl (Handshake):** `None` (Default), `XON/XOFF` (Software), `RTS/CTS` (Hardware)

## 3. Eksekusi
1. Membuat UI 2 tingkat di `ui/interface.py`.
2. Menyisipkan fungsi konverter Hex dari UI input sebelum dilempar (`main.py`).
3. Menggunakan argumentasi Textual `Checkbox` untuk mentransmisikan status `Hex Rcv` ke method parser secara langsung.
4. Menambahkan properti koneksi ke file PySerial `serial_handler.py`.

---

**Pertanyaan:** Apakah Anda setuju dengan desain UI **Dua Baris (2 Rows)** seperti gambaran di atas? Jika setuju (silakan jawab "Ya/Setuju/Lanjut"), saya akan langsung menulis (*Generate*) fungsinya ke dalam modul-modul yang ada.
