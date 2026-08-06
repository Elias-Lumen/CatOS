import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "CatOS.db"



def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    # Allow query results to be accessed as user["username"]
    # instead of user[1].
    connection.row_factory = sqlite3.Row

    # Enable foreign key constraints in SQLite.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# User table use for store users' id and avatar
def create_users_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            avatar_url TEXT
        )
    """)


# tasks
def create_tasks_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            tag TEXT,

            state TEXT NOT NULL DEFAULT 'not_started'
                CHECK (
                    state IN (
                        'not_started',
                        'in_progress',
                        'completed'
                    )
                ),

            priority TEXT NOT NULL DEFAULT 'medium'
                CHECK (
                    priority IN (
                        'low',
                        'medium',
                        'high'
                    )
                ),

            due_date TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


# subtask
def create_subtasks_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS subtasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            tag TEXT,

            state TEXT NOT NULL DEFAULT 'not_started'
                CHECK (
                    state IN (
                        'not_started',
                        'in_progress',
                        'completed'
                    )
                ),

            priority TEXT NOT NULL DEFAULT 'medium'
                CHECK (
                    priority IN (
                        'low',
                        'medium',
                        'high'
                    )
                ),

            due_date TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,

            FOREIGN KEY (task_id)
                REFERENCES tasks(id)
                ON DELETE CASCADE
        )
    """)

# cats
def create_cat_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS cat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            cat_name TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'idle',

            mood INTEGER NOT NULL DEFAULT 50
                CHECK (mood BETWEEN 0 AND 100),

            energy INTEGER NOT NULL DEFAULT 100
                CHECK (energy BETWEEN 0 AND 100),

            hunger INTEGER NOT NULL DEFAULT 0
                CHECK (hunger BETWEEN 0 AND 100),

            last_interaction TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP,

            equipped_item TEXT,
            cat_color TEXT,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


def create_tables():
    connection = get_connection()

    try:
        create_users_table(connection)
        create_tasks_table(connection)
        create_subtasks_table(connection)
        create_cat_table(connection)

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()