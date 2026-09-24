"""Create the tables used by the CatOS database."""

import sqlite3

from .connection import get_connection


def create_users_table(connection):
    """Create the users table if it does not exist yet."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            avatar_url TEXT
        )
    """)


def create_tasks_table(connection):
    """Create the tasks table if it does not exist yet."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,

            -- task can only have one of these three states
            state TEXT NOT NULL DEFAULT 'not_started'
                CHECK (
                    state IN (
                        'not_started',
                        'in_progress',
                        'completed'
                    )
                ),

            -- normal is the default if the user does not choose a priority
            priority TEXT NOT NULL DEFAULT 'normal'
                CHECK (
                    priority IN (
                        'normal',
                        'low',
                        'medium',
                        'high'
                    )
                ),

            start_date DATE,
            due_date DATE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,

            -- connect the task to its user
            -- if the user is deleted, their tasks should also be deleted
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


def create_tags_table(connection):
    """Create the tags table if it does not exist yet."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,

            -- one user cannot create two tags with exactly the same name
            UNIQUE (user_id, name),

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


def create_task_tags_table(connection):
    """Create the junction table between tasks and tags."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS task_tags (
            task_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,

            -- both values together make one unique relationship
            PRIMARY KEY (task_id, tag_id),

            FOREIGN KEY (task_id)
                REFERENCES tasks(id)
                ON DELETE CASCADE,

            FOREIGN KEY (tag_id)
                REFERENCES tags(id)
                ON DELETE CASCADE
        )
    """)


def create_subtasks_table(connection):
    """Create the subtasks table if it does not exist yet."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS subtasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,

            -- use the same states as the main tasks
            state TEXT NOT NULL DEFAULT 'not_started'
                CHECK (
                    state IN (
                        'not_started',
                        'in_progress',
                        'completed'
                    )
                ),

            -- subtasks can have their own priority
            priority TEXT NOT NULL DEFAULT 'normal'
                CHECK (
                    priority IN (
                        'normal',
                        'low',
                        'medium',
                        'high'
                    )
                ),

            due_date TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,

            -- connect the subtask to its main task
            -- deleting the main task will also delete its subtasks
            FOREIGN KEY (task_id)
                REFERENCES tasks(id)
                ON DELETE CASCADE
        )
    """)


def create_cat_table(connection):
    """Create the virtual cat table if it does not exist yet."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS cat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            cat_name TEXT NOT NULL,

            -- what the cat is doing at the moment
            status TEXT NOT NULL DEFAULT 'idle',

            -- keep these values between 0 and 100
            mood INTEGER NOT NULL DEFAULT 50
                CHECK (mood BETWEEN 0 AND 100),

            energy INTEGER NOT NULL DEFAULT 100
                CHECK (energy BETWEEN 0 AND 100),

            hunger INTEGER NOT NULL DEFAULT 0
                CHECK (hunger BETWEEN 0 AND 100),

            -- remember when the user last interacted with their cat
            last_interaction TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP,

            equipped_item TEXT,
            cat_color TEXT,

            -- connect the cat to its owner
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


def create_tables():
    """Create all CatOS tables without replacing existing ones."""

    connection = get_connection()

    try:
        create_users_table(connection)
        create_tasks_table(connection)
        create_tags_table(connection)
        create_task_tags_table(connection)
        create_subtasks_table(connection)
        create_cat_table(connection)

        # Save all table changes together.
        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# This only runs when tables.py is run directly.
if __name__ == "__main__":
    create_tables()
