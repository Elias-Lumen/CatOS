import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "flowist.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    # 让查询结果可以写成 user["username"]
    # 而不是 user[1]
    connection.row_factory = sqlite3.Row

    return connection


def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()