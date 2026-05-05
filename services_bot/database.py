import sqlite3
from typing import List
from config import DB_PATH


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def add_user(self, user_id: int, username: str) -> bool:
        """Добавляет пользователя, если его ещё нет. Возвращает True, если добавлен."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                    (user_id, username)
                )
                return cursor.rowcount == 1
        except Exception as e:
            print(f"Ошибка при добавлении пользователя {user_id}: {e}")
            return False

    def user_exists(self, user_id: int) -> bool:
        """Проверяет, существует ли пользователь"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE user_id = ? LIMIT 1", (user_id,))
            return cursor.fetchone() is not None

    def get_all_user_ids(self) -> List[int]:
        """Возвращает список всех user_id"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users")
            return [row[0] for row in cursor.fetchall()]

    def update_username(self, user_id: int, username: str):
        """Обновляет username"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET username = ? WHERE user_id = ?",
                (username, user_id)
            )

db = Database()