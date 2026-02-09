from typing import List, Optional, Dict
from .database import get_db

class CommandRepository:
    @staticmethod
    def create(command_name: str, command_path: str, is_preset: bool = False) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO commands (command_name, command_path, is_preset) VALUES (?, ?, ?)",
                (command_name, command_path, 1 if is_preset else 0)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all() -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM commands ORDER BY command_name")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_name(command_name: str) -> Optional[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM commands WHERE command_name = ?", (command_name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update(command_name: str, command_path: str) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE commands SET command_path = ? WHERE command_name = ?",
                (command_path, command_name)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(command_name: str) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM commands WHERE command_name = ? AND is_preset = 0", (command_name,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def get_command_dict() -> Dict[str, str]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT command_name, command_path FROM commands")
            return {row["command_name"]: row["command_path"] for row in cursor.fetchall()}

class SettingsRepository:
    @staticmethod
    def get(key: str) -> Optional[str]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row["value"] if row else None

    @staticmethod
    def set(key: str, value: str):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, value)
            )
            conn.commit()

    @staticmethod
    def get_all() -> Dict[str, str]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM settings")
            return {row["key"]: row["value"] for row in cursor.fetchall()}
