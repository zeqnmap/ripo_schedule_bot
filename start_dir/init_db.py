import sqlite3


def init_database():
    conn = sqlite3.connect('../users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ База данных создана")


if __name__ == '__main__':
    init_database()