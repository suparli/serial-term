import sqlite3
import datetime
from utils.config import DB_FILE, ensure_directories

class Database:
    def __init__(self):
        ensure_directories()
        self.conn = sqlite3.connect(DB_FILE)
        self._init_tables()

    def _init_tables(self):
        cursor = self.conn.cursor()
        # Table command_history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')
        # Table custom_commands
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias TEXT UNIQUE NOT NULL,
                payload TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()

    def log_command(self, command: str):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO command_history (command, timestamp) VALUES (?, ?)',
            (command, datetime.datetime.now())
        )
        self.conn.commit()

    def get_history(self, limit: int = 100) -> list:
        cursor = self.conn.cursor()
        # Reverse order, so we get oldest to newest of the last N
        cursor.execute('SELECT command FROM command_history ORDER BY id DESC LIMIT ?', (limit,))
        return [row[0] for row in reversed(cursor.fetchall())]

    def add_custom_command(self, alias: str, payload: str, description: str = ""):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO custom_commands (alias, payload, description) VALUES (?, ?, ?)',
                (alias, payload, description)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Alias exists

    def get_custom_command(self, alias: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute('SELECT payload FROM custom_commands WHERE alias = ?', (alias,))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_all_custom_commands(self) -> list:
        cursor = self.conn.cursor()
        cursor.execute('SELECT alias, payload, description FROM custom_commands ORDER BY alias ASC')
        return cursor.fetchall()

    def close(self):
        self.conn.close()
