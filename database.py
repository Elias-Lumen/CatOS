import sqlite3
from pathlib import Path


# find where this python file is, then find CatOS.db from the same folder
# this makes the database path still work if the project is moved somewhere else
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "CatOS.db"       # will genernal the db file


# connect to the CatOS database
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    # make the results easier to read
    # for example, use user["username"] instead of user[1]
    connection.row_factory = sqlite3.Row

    # SQLite does not turn foreign keys on automatically
    # this makes the relationships between the tables actually work
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# users table
# stores the login information and profile picture for each user
def create_users_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            avatar_url TEXT
        )
    """)


# tasks table
# every task belongs to one user by using user_id
def create_tasks_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            tag TEXT,

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

            due_date TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,

            -- connect the task to its user
            -- if the user is deleted, their tasks should also be deleted
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


# subtasks table
# similar to tasks, but every subtask belongs to a main task
# if a task has no subtasks, there just will not be any rows for it here
def create_subtasks_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS subtasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            tag TEXT,

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


# cat table
# each user can have one cat, so user_id needs to be unique here
def create_cat_table(connection):
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


# get one user's information using their id
# mainly useful when I need their username or avatar
def get_user_by_id(user_id):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT
            id,
            username,
            avatar_url
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return user


# change the saved avatar path for one user
def update_user_avatar(user_id, avatar_url):
    connection = get_connection()

    try:
        # only update the user that is currently logged in
        connection.execute(
            """
            UPDATE users
            SET avatar_url = ?
            WHERE id = ?
            """,
            (
                avatar_url,
                user_id
            )
        )

        # actually save the change
        connection.commit()

    except sqlite3.Error:
        # if something goes wrong, cancel the unfinished change
        connection.rollback()
        raise

    finally:
        # close the connection whether it worked or not
        connection.close()


# create a new task for a user
def create_task(
    user_id,
    title,
    description=None,
    tag=None,
    state="not_started",
    priority="normal",
    due_date=None
):
    connection = get_connection()

    try:
        # add all the task information into a new row
        connection.execute(
            """
            INSERT INTO tasks (
                user_id,
                title,
                description,
                tag,
                state,
                priority,
                due_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                title,
                description,
                tag,
                state,
                priority,
                due_date
            )
        )

        # save the new task
        connection.commit()

    except sqlite3.Error:
        # do not leave a half-finished change in the database
        connection.rollback()
        raise

    finally:
        connection.close()


# get all tasks that belong to one user
def get_tasks_by_user(user_id):
    connection = get_connection()

    tasks = connection.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id = ?
        ORDER BY
            CASE
                WHEN state = 'completed' THEN 1
                ELSE 0
            END,

            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
                WHEN 'normal' THEN 4
            END,

            created_at DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return tasks



def toggle_task_completion(task_id, user_id):
    connection = get_connection()

    try:
        task = connection.execute(
            """
            SELECT state
            FROM tasks
            WHERE id = ? AND user_id = ?
            """,
            (task_id, user_id)
        ).fetchone()

        if task is None:
            return False

        if task["state"] == "completed":
            new_state = "not_started"

            connection.execute(
                """
                UPDATE tasks
                SET state = ?,
                    completed_at = NULL
                WHERE id = ? AND user_id = ?
                """,
                (
                    new_state,
                    task_id,
                    user_id
                )
            )

        else:
            new_state = "completed"

            connection.execute(
                """
                UPDATE tasks
                SET state = ?,
                    completed_at = CURRENT_TIMESTAMP
                WHERE id = ? AND user_id = ?
                """,
                (
                    new_state,
                    task_id,
                    user_id
                )
            )

        connection.commit()
        return True

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def update_task(
    task_id,
    user_id,
    title,
    description=None,
    priority="normal",
    due_date=None
):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE tasks
            SET
                title = ?,
                description = ?,
                priority = ?,
                due_date = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                title,
                description,
                priority,
                due_date,
                task_id,
                user_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()

def delete_task(task_id, user_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM tasks
            WHERE id = ? AND user_id = ?
            """,
            (
                task_id,
                user_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()
        
# put any new database functions above this part


# create all the tables when CatOS first starts
# CREATE TABLE IF NOT EXISTS means existing tables will not be replaced
def create_tables():
    connection = get_connection()

    try:
        create_users_table(connection)
        create_tasks_table(connection)
        create_subtasks_table(connection)
        create_cat_table(connection)

        # save all table changes together
        connection.commit()

    except sqlite3.Error:
        # cancel the changes if one of the table creations fails
        connection.rollback()
        raise

    finally:
        connection.close()


# this only runs when database.py is run directly
# useful if I want to create/check the tables without starting the Flask app
if __name__ == "__main__":
    create_tables()