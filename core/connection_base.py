import asyncio
from abc import ABC, abstractmethod

class ConnectionBase(ABC):
    def __init__(self):
        self.is_connected = False
        self.rx_queue = asyncio.Queue()

    @abstractmethod
    async def connect(self, target: str, **kwargs) -> tuple[bool, str]:
        """Konek ke target (Port COM atau MAC BLE). Return (sukses, pesan_error)"""
        pass

    @abstractmethod
    async def disconnect(self):
        """Putus koneksi"""
        pass

    @abstractmethod
    async def write(self, data: bytes) -> bool:
        """Kirim data string/bytes"""
        pass

    async def read_loop(self):
        """Membaca stream secara terus menerus (harus dijalankan sebagai background task)"""
        pass
