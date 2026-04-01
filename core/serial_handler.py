import asyncio
import serial
from .connection_base import ConnectionBase

class SerialHandler(ConnectionBase):
    def __init__(self):
        super().__init__()
        self.ser = None
        self._read_task = None

    async def connect(self, target: str, baudrate: int = 115200, bytesize: int = 8, parity: str = 'N', stopbits: float = 1, xonxoff: bool = False, rtscts: bool = False, **kwargs) -> tuple[bool, str]:
        if self.is_connected:
            await self.disconnect()
        
        try:
            self.ser = await asyncio.to_thread(
                serial.Serial, port=target, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, xonxoff=xonxoff, rtscts=rtscts, timeout=0.1
            )
            self.is_connected = True
            
            # Start background reading
            self._read_task = asyncio.create_task(self.read_loop())
            return True, ""
        except Exception as e:
            return False, f"Serial Connection Error: {e}"

    async def disconnect(self):
        self.is_connected = False
        if self._read_task:
            self._read_task.cancel()
            self._read_task = None
            
        if self.ser and self.ser.is_open:
            await asyncio.to_thread(self.ser.close)

    async def write(self, data: bytes) -> bool:
        if not self.is_connected or not self.ser:
            return False
            
        try:
            await asyncio.to_thread(self.ser.write, data)
            return True
        except Exception as e:
            # Drop connection on write error
            await self.disconnect()
            return False

    async def read_loop(self):
        while self.is_connected:
            try:
                # Check bytes in waiting before reading to prevent blocking
                in_waiting = await asyncio.to_thread(lambda: getattr(self.ser, 'in_waiting', 0))
                if in_waiting > 0:
                    data = await asyncio.to_thread(self.ser.read, in_waiting)
                    if data:
                        await self.rx_queue.put(data)
                else:
                    await asyncio.sleep(0.01)
            except Exception as e:
                await self.disconnect()
                break
