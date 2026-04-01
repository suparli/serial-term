from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import RichLog, Select, Button, Static, OptionList, Label, Checkbox
from .components import HistoryInput
from core.database import Database

class TerminalUI(Container):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        
    def compose(self) -> ComposeResult:
        with Horizontal(id="top-bar", classes="mb-1"):
            yield Select([], prompt="Select Device", id="device-select")
            yield Button("Connect", id="btn-connect", variant="success")
            yield Button("Scan Devices", id="btn-scan", variant="primary")
            yield Static("Status: Disconnected", id="status-label")
        with Horizontal(id="serial-settings", classes="mb-1"):
            yield Select([("9600", 9600), ("19200", 19200), ("38400", 38400), ("57600", 57600), ("115200", 115200), ("230400", 230400)], prompt="BaudRate", value=115200, id="baudrate-select")
            yield Select([("5", 5), ("6", 6), ("7", 7), ("8", 8)], prompt="DataBits", value=8, id="databits-select")
            yield Select([("None", "N"), ("Even", "E"), ("Odd", "O"), ("Mark", "M"), ("Space", "S")], prompt="Parity", value="N", id="parity-select")
            yield Select([("1", 1), ("1.5", 1.5), ("2", 2)], prompt="StopBits", value=1, id="stopbits-select")
            yield Select([("None", "none"), ("XON/XOFF", "xonxoff"), ("RTS/CTS", "rtscts")], prompt="FlowCtrl", value="none", id="flowctrl-select")
            yield Checkbox("Hex Receive", id="hex-receive")
            yield Checkbox("Hex Send", id="hex-send")

        with Horizontal(id="main-layout"):
            with Vertical(id="main-area"):
                yield RichLog(id="data-log", highlight=True, markup=True, auto_scroll=True, wrap=True)
                yield HistoryInput(self.db, placeholder="Ketik perintah biasa, atau buat baru: /addmacro namamacro perintah", id="cmd-input")
            with Vertical(id="macro-sidebar"):
                yield Label("Custom Macros", id="macro-title")
                yield OptionList(id="macro-list")
