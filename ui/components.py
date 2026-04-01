from textual.widgets import Input
from textual.binding import Binding
from core.database import Database

class HistoryInput(Input):
    """Input bar with Up/Down arrow history navigation"""
    
    BINDINGS = [
        Binding("up", "history_up", "Previous Command"),
        Binding("down", "history_down", "Next Command"),
    ]

    def __init__(self, db: Database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db
        self.history = []
        self.history_index = -1

    def on_mount(self):
        # Load recent history from DB
        self.history = self.db.get_history(limit=50)
        self.history_index = len(self.history)
        
    def add_to_history(self, command: str):
        if command and (not self.history or self.history[-1] != command):
            self.history.append(command)
        self.history_index = len(self.history)

    def action_history_up(self):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)

    def action_history_down(self):
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)
        elif self.history_index == len(self.history) - 1:
            self.history_index = len(self.history)
            self.value = ""
