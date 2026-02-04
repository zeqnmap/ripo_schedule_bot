import sqlite3
from typing import List
from config import DB_PATH

def take_users_id() -> List[int]:
    """Берет из БД SQLite колонку с id юзеров с помощью SQL запроса"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users;")
    ids = cursor.fetchall()
    all_id: List[int] = [row[0] for row in ids]
    return all_id