import sys
import asyncio
from bleak import BleakClient, BleakError

async def explore_device(mac_address: str):
    print(f"Mencoba menyambungkan ke {mac_address}...")
    try:
        async with BleakClient(mac_address, timeout=10.0) as client:
            print("Berhasil Terhubung!\n")
            print("--- Daftar Layanan (Services) & Karakteristik (Characteristics) ---")
            for service in client.services:
                print(f"\n[Service] {service.uuid}: {service.description}")
                for char in service.characteristics:
                    print(f"  └─ [Characteristic] {char.uuid}")
                    print(f"       Deskripsi  : {char.description}")
                    print(f"       Properti   : {', '.join(char.properties)}")
                    
            print("\n-----------------------------------------------------------")
            print("TIPS: Cari 'Characteristic' yang memiliki properti 'write' atau 'write-without-response' (untuk TX) dan properti 'notify' (untuk RX).")
    except BleakError as e:
        print(f"Gagal Terhubung: {e}")
    except Exception as e:
        print(f"Error tidak di kenal: {e}")

if __name__ == "__main__":
    default_mac = "48:87:2D:81:AA:86" # Diambil dari catatan log pengguna
    # Argument passing support, misal: python discover_ble.py AA:BB:CC
    target_mac = sys.argv[1] if len(sys.argv) > 1 else default_mac
    
    asyncio.run(explore_device(target_mac))
