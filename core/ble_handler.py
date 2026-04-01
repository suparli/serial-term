import asyncio
from bleak import BleakClient, BleakError
from .connection_base import ConnectionBase

# HM-10 / JDY-08 Default BLE Serial UUIDs
UART_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
UART_TX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

class BLEHandler(ConnectionBase):
    def __init__(self):
        super().__init__()
        self.client = None
        self.rx_char = None
        self.tx_char = None

    def notification_handler(self, sender, data: bytearray):
        """Callback for bleak notifications"""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.rx_queue.put(bytes(data)))
        except Exception:
            pass

    async def connect(self, target: str, **kwargs) -> tuple[bool, str]:
        if self.is_connected:
            await self.disconnect()

        try:
            self.client = BleakClient(target)
            await self.client.connect()
            self.is_connected = True
            
            rx_uuid = kwargs.get('rx_uuid', UART_RX_CHAR_UUID)
            tx_uuid = kwargs.get('tx_uuid', UART_TX_CHAR_UUID)

            # Start notifications
            await self.client.start_notify(tx_uuid, self.notification_handler)
            self.rx_char = rx_uuid
            self.tx_char = tx_uuid

            return True, ""
        except Exception as e:
            return False, f"BLE Exception: {e}"

    async def disconnect(self):
        self.is_connected = False
        if self.client and self.client.is_connected:
            try:
                if self.tx_char:
                    await self.client.stop_notify(self.tx_char)
                await self.client.disconnect()
            except Exception:
                pass

    async def write(self, data: bytes) -> bool:
        if not self.is_connected or not self.client:
            return False
            
        try:
            await self.client.write_gatt_char(self.rx_char, data, response=False)
            return True
        except Exception as e:
            await self.disconnect()
            return False
