import asyncio
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Input, Select, Button, OptionList, Checkbox
from ui.interface import TerminalUI
from ui.formatter import format_log
from core.database import Database
from core.serial_handler import SerialHandler
from core.ble_handler import BLEHandler
import serial.tools.list_ports
from bleak import BleakScanner
from utils.config import LOGS_DIR

class MultiSerialTerm(App):
    CSS = """
    #top-bar {
        height: 3;
        align: left middle;
    }
    #serial-settings {
        height: 3;
        align: left middle;
    }
    #device-select {
        width: 40;
    }
    #btn-connect, #btn-scan {
        margin-left: 1;
    }
    #status-label {
        color: red;
        margin-left: 2;
        padding-top: 1;
    }
    #status-label.connected {
        color: green;
    }
    #main-layout {
        height: 1fr;
    }
    #main-area {
        width: 75%;
        height: 100%;
    }
    #macro-sidebar {
        width: 25%;
        height: 100%;
        border-left: solid white;
        padding-left: 1;
        padding-right: 1;
    }
    #macro-title {
        text-align: center;
        text-style: bold;
        color: yellow;
        margin-bottom: 1;
    }
    #macro-list {
        height: 1fr;
    }
    #cmd-input {
        dock: bottom;
    }
    #data-log {
        height: 1fr;
        background: $surface;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f5", "scan", "Scan Devices (F5)"),
        ("f6", "toggle_connect", "Connect/Disconnect (F6)"),
    ]

    async def action_scan(self):
        self.write_log("[System] Keyboard Shortcut (F5) Ditekan - Pindai Alat")
        await self.scan_devices()

    async def action_toggle_connect(self):
        self.write_log("[System] Keyboard Shortcut (F6) Ditekan - Toggle Koneksi")
        await self.toggle_connection()

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.handler = None
        self._read_task = None
        self.logger_file = None

    def write_log(self, text: str):
        log_widget = self.query_one("#data-log", RichLog)
        log_widget.write(text)
        try:
            if not self.logger_file or self.logger_file.closed:
                LOGS_DIR.mkdir(parents=True, exist_ok=True)
                self.logger_file = open(LOGS_DIR / "session.log", "a", encoding="utf-8")
            self.logger_file.write(str(text) + "\n")
            self.logger_file.flush()
        except:
            pass

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TerminalUI(self.db)
        yield Footer()

    def refresh_macros(self):
        macro_list = self.query_one("#macro-list", OptionList)
        macro_list.clear_options()
        macros = self.db.get_all_custom_commands()
        if not macros:
            macro_list.add_option("Ketik: /addmacro (alias) (isi) di bar input")
            return

        for alias, payload, desc in macros:
            macro_list.add_option(f"[{alias}] {payload}")

    def on_mount(self):
        self.title = "Multi-Serial Terminal"
        self.write_log("[System] Berhasil dimuat. Auto-Save log sedang berjalan ('logs/session.log').")
        self.refresh_macros()

    async def on_button_pressed(self, event):
        if event.button.id == "btn-scan":
            await self.scan_devices()
        elif event.button.id == "btn-connect":
            await self.toggle_connection()

    @on(OptionList.OptionSelected, "#macro-list")
    async def on_macro_selected(self, event: OptionList.OptionSelected):
        # Saat salah satu makro di klik Enter pada OptionList
        text = str(event.option.prompt)
        
        # Contoh bentuk: "[alias] payload..."
        if text.startswith("[") and "]" in text:
            alias = text.split("]")[0][1:]
            payload = self.db.get_custom_command(alias)
            
            if self.handler and self.handler.is_connected:
                self.write_log(f"> [Di-klik lewat Macro Panel] {alias}")
                hex_send = self.query_one("#hex-send", Checkbox).value
                if hex_send:
                    try:
                        data_to_send = bytes.fromhex(payload)
                    except ValueError:
                        self.write_log("[System] Error: Invalid hex string for macro.")
                        return
                else:
                    data_to_send = (payload + "\n").encode('utf-8')
                await self.handler.write(data_to_send)
            else:
                self.write_log("[System] Cannot send macro: Not connected.")

    async def scan_devices(self):
        select = self.query_one("#device-select", Select)
        self.write_log("[Scanning...] Looking for serial ports and BLE devices...")
        options = []
        
        com_ports = serial.tools.list_ports.comports()
        for port in com_ports:
            options.append((f"[USB] {port.device} - {port.description}", f"USB|{port.device}"))
            
        try:
            ble_devices = await BleakScanner.discover(timeout=3.0)
            for d in ble_devices:
                name = d.name or "Unknown"
                options.append((f"[BLE] {name} ({d.address})", f"BLE|{d.address}"))
        except Exception as e:
            self.write_log(f"[Error] BLE Scan failed (Ensure Bluetooth is on): {e}")
            
        select.set_options(options)
        self.write_log(f"[System] Found {len(com_ports)} USB and {len(options) - len(com_ports)} BLE devices.")

    async def toggle_connection(self):
        btn = self.query_one("#btn-connect", Button)
        status = self.query_one("#status-label")
        select = self.query_one("#device-select", Select)

        if self.handler and self.handler.is_connected:
            await self.handler.disconnect()
            btn.label = "Connect"
            btn.variant = "success"
            status.update("Status: Disconnected")
            status.remove_class("connected")
            self.write_log("[System] Disconnected.")
            if self._read_task:
                self._read_task.cancel()
        else:
            if not select.value:
                self.write_log("[System] Please select a device first.")
                return

            dev_type, dev_addr = select.value.split("|")
            
            if dev_type == "USB":
                baudrate = self.query_one("#baudrate-select", Select).value
                databits = self.query_one("#databits-select", Select).value
                parity = self.query_one("#parity-select", Select).value
                stopbits = self.query_one("#stopbits-select", Select).value
                flowctrl = self.query_one("#flowctrl-select", Select).value
                
                kwargs = {
                    "baudrate": baudrate if baudrate else 115200,
                    "bytesize": databits if databits else 8,
                    "parity": parity if parity else 'N',
                    "stopbits": stopbits if stopbits else 1,
                    "xonxoff": flowctrl == "xonxoff",
                    "rtscts": flowctrl == "rtscts"
                }
                
                self.handler = SerialHandler()
                self.write_log(f"[System] Connecting to USB {dev_addr} with {kwargs}...")
                success, msg = await self.handler.connect(dev_addr, **kwargs)
            else:
                self.handler = BLEHandler()
                self.write_log(f"[System] Connecting to BLE {dev_addr}...")
                success, msg = await self.handler.connect(dev_addr)

            if success:
                btn.label = "Disconnect"
                btn.variant = "error"
                status.update(f"Status: Connected ({dev_type})")
                status.add_class("connected")
                self.write_log("[System] Connection Established.")
                self._read_task = asyncio.create_task(self.read_from_device())
            else:
                self.write_log(f"[Error] Connection Failed: {msg}")

    async def read_from_device(self):
        try:
            while self.handler and self.handler.is_connected:
                data = await self.handler.rx_queue.get()
                hex_rcv = self.query_one("#hex-receive", Checkbox).value
                self.write_log(format_log(data, as_hex=hex_rcv))
        except asyncio.CancelledError:
            pass

    async def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "cmd-input":
            command = event.value.strip()
            if not command:
                return

            # Cek form pembuatan marco "/addmacro namamacro AT+COM"
            if command.startswith("/addmacro "):
                parts = command.split(" ", 2)
                if len(parts) >= 3:
                    alias = parts[1]
                    payload = parts[2]
                    self.db.add_custom_command(alias, payload)
                    self.write_log(f"[System] Makro baru tersimpan! ({alias} -> {payload})")
                    self.refresh_macros()
                else:
                    self.write_log("[System] Format membuat macro salah. Gunakan: /addmacro namamacro isi_perintah")
                event.input.value = ""
                return

            # Cek penggunaan makro lama
            p_command = command
            if command.startswith("/"):
                alias = command[1:]
                payload = self.db.get_custom_command(alias)
                if payload:
                    p_command = payload
                else:
                    self.write_log(f"[System] Unknown macro: {command}")
                    event.input.value = ""
                    return

            self.db.log_command(command)
            event.input.add_to_history(command)
            self.write_log(f"> {command}")
            
            if self.handler and self.handler.is_connected:
                hex_send = self.query_one("#hex-send", Checkbox).value
                if hex_send:
                    try:
                        data_to_send = bytes.fromhex(p_command)
                    except ValueError:
                        self.write_log("[System] Error: Invalid hex string.")
                        event.input.value = ""
                        return
                else:
                    data_to_send = (p_command + "\n").encode('utf-8')
                await self.handler.write(data_to_send)
            else:
                self.write_log("[System] Cannot send: Not connected.")
                
            event.input.value = ""

    async def on_unmount(self):
        if self.handler:
            await self.handler.disconnect()
        if self.logger_file:
            self.logger_file.close()
        self.db.close()

if __name__ == "__main__":
    app = MultiSerialTerm()
    app.run()
