import sqlite3
from pathlib import Path


# find where this python file is, then find CatOS.db from the same folder
# this makes the database path still work if the project is moved somewhere else
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "CatOS.db"       # will generate the db file


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


# tags table
# every tag belongs to one user
def create_tags_table(connection):
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


# task_tags is the junction table between tasks and tags
# one task can have many tags, and one tag can belong to many tasks
def create_task_tags_table(connection):
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

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# create a new task for a user
# return the new task id so tags can be attached to it afterwards
def create_task(
    user_id,
    title,
    description=None,
    state="not_started",
    priority="normal",
    start_date=None,
    due_date=None
):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO tasks (
                user_id,
                title,
                description,
                state,
                priority,
                start_date,
                due_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                title,
                description,
                state,
                priority,
                start_date,
                due_date
            )
        )

        task_id = cursor.lastrowid

        connection.commit()

        return task_id

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# create a new tag for one user
# if the same tag already exists, return its id instead
def create_tag(user_id, name):
    connection = get_connection()

    try:
        existing_tag = connection.execute(
            """
            SELECT id
            FROM tags
            WHERE user_id = ? AND name = ?
            """,
            (
                user_id,
                name
            )
        ).fetchone()

        if existing_tag:
            return existing_tag["id"]

        cursor = connection.execute(
            """
            INSERT INTO tags (
                user_id,
                name
            )
            VALUES (?, ?)
            """,
            (
                user_id,
                name
            )
        )

        tag_id = cursor.lastrowid

        connection.commit()

        return tag_id

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# get all tags that belong to one user
def get_tags_by_user(user_id):
    connection = get_connection()

    tags = connection.execute(
        """
        SELECT
            id,
            name
        FROM tags
        WHERE user_id = ?
        ORDER BY name COLLATE NOCASE
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return tags


# Get all tasks using one label.
def get_tasks_by_tag(
    user_id,
    tag_id
):

    connection = get_connection()

    tasks = connection.execute(
        """
        SELECT tasks.*
        FROM tasks

        JOIN task_tags
            ON task_tags.task_id = tasks.id

        JOIN tags
            ON tags.id = task_tags.tag_id

        WHERE
            tasks.user_id = ?
            AND tags.user_id = ?
            AND tags.id = ?

        ORDER BY
            CASE
                WHEN tasks.state = 'completed' THEN 1
                ELSE 0
            END,

            CASE tasks.priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
                WHEN 'normal' THEN 4
            END,

            tasks.created_at DESC
        """,
        (
            user_id,
            user_id,
            tag_id
        )
    ).fetchall()

    connection.close()

    return tasks


# Rename one label.
def update_tag(
    tag_id,
    user_id,
    name
):

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            UPDATE tags
            SET name = ?
            WHERE
                id = ?
                AND user_id = ?
            """,
            (
                name,
                tag_id,
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


# Delete a label without deleting its tasks.
def delete_tag(
    tag_id,
    user_id
):

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            DELETE FROM tags
            WHERE
                id = ?
                AND user_id = ?
            """,
            (
                tag_id,
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



# get all tags attached to one task
# also checks that the task belongs to the current user
def get_tags_by_task(task_id, user_id):
    connection = get_connection()

    tags = connection.execute(
        """
        SELECT
            tags.id,
            tags.name
        FROM tags

        JOIN task_tags
            ON task_tags.tag_id = tags.id

        JOIN tasks
            ON tasks.id = task_tags.task_id

        WHERE
            task_tags.task_id = ?
            AND tasks.user_id = ?

        ORDER BY tags.name COLLATE NOCASE
        """,
        (
            task_id,
            user_id
        )
    ).fetchall()

    connection.close()

    return tags


# replace all tag relationships for one task
def set_task_tags(task_id, user_id, tag_ids):
    connection = get_connection()

    try:
        task = connection.execute(
            """
            SELECT id
            FROM tasks
            WHERE id = ? AND user_id = ?
            """,
            (
                task_id,
                user_id
            )
        ).fetchone()

        if task is None:
            return False

        connection.execute(
            """
            DELETE FROM task_tags
            WHERE task_id = ?
            """,
            (task_id,)
        )

        for tag_id in tag_ids:

            tag = connection.execute(
                """
                SELECT id
                FROM tags
                WHERE id = ? AND user_id = ?
                """,
                (
                    tag_id,
                    user_id
                )
            ).fetchone()

            if tag:
                connection.execute(
                    """
                    INSERT INTO task_tags (
                        task_id,
                        tag_id
                    )
                    VALUES (?, ?)
                    """,
                    (
                        task_id,
                        tag_id
                    )
                )

        connection.commit()

        return True

    except sqlite3.Error:
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
    start_date=None,
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
                start_date = ?,
                due_date = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                title,
                description,
                priority,
                start_date,
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


# SUBTASKS


# create a subtask under a task
# also checks that the parent task belongs to the current user
def create_subtask(
    task_id,
    user_id,
    title,
    description=None,
    priority="normal",
    due_date=None
):
    connection = get_connection()

    try:
        task = connection.execute(
            """
            SELECT id
            FROM tasks
            WHERE id = ? AND user_id = ?
            """,
            (
                task_id,
                user_id
            )
        ).fetchone()

        if task is None:
            return None

        cursor = connection.execute(
            """
            INSERT INTO subtasks (
                task_id,
                title,
                description,
                priority,
                due_date
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                task_id,
                title,
                description,
                priority,
                due_date
            )
        )

        subtask_id = cursor.lastrowid

        connection.commit()

        return subtask_id

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# get all subtasks under one task
# user_id protects tasks from being read by another logged-in user
def get_subtasks_by_task(task_id, user_id):
    connection = get_connection()

    subtasks = connection.execute(
        """
        SELECT
            subtasks.*
        FROM subtasks

        JOIN tasks
            ON tasks.id = subtasks.task_id

        WHERE
            subtasks.task_id = ?
            AND tasks.user_id = ?

        ORDER BY
            CASE
                WHEN subtasks.state = 'completed' THEN 1
                ELSE 0
            END,
            subtasks.created_at ASC
        """,
        (
            task_id,
            user_id
        )
    ).fetchall()

    connection.close()

    return subtasks


# toggle a subtask between completed and not started
def toggle_subtask_completion(
    subtask_id,
    user_id
):
    connection = get_connection()

    try:
        subtask = connection.execute(
            """
            SELECT
                subtasks.id,
                subtasks.state
            FROM subtasks

            JOIN tasks
                ON tasks.id = subtasks.task_id

            WHERE
                subtasks.id = ?
                AND tasks.user_id = ?
            """,
            (
                subtask_id,
                user_id
            )
        ).fetchone()

        if subtask is None:
            return False

        if subtask["state"] == "completed":
            new_state = "not_started"

            connection.execute(
                """
                UPDATE subtasks
                SET
                    state = ?,
                    completed_at = NULL
                WHERE id = ?
                """,
                (
                    new_state,
                    subtask_id
                )
            )

        else:
            new_state = "completed"

            connection.execute(
                """
                UPDATE subtasks
                SET
                    state = ?,
                    completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    new_state,
                    subtask_id
                )
            )

        connection.commit()

        return True

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# update the information of one subtask
def update_subtask(
    subtask_id,
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
            UPDATE subtasks
            SET
                title = ?,
                description = ?,
                priority = ?,
                due_date = ?
            WHERE id IN (
                SELECT subtasks.id
                FROM subtasks

                JOIN tasks
                    ON tasks.id = subtasks.task_id

                WHERE
                    subtasks.id = ?
                    AND tasks.user_id = ?
            )
            """,
            (
                title,
                description,
                priority,
                due_date,
                subtask_id,
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


# delete one subtask
def delete_subtask(
    subtask_id,
    user_id
):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM subtasks
            WHERE id IN (
                SELECT subtasks.id
                FROM subtasks

                JOIN tasks
                    ON tasks.id = subtasks.task_id

                WHERE
                    subtasks.id = ?
                    AND tasks.user_id = ?
            )
            """,
            (
                subtask_id,
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


# Search one user's tasks.
# Every filter is optional, so the same function can handle simple
# searches and more specific searches.
def search_tasks(
    user_id,
    query="",
    tag_id=None,
    priority=None,
    state=None
):

    connection = get_connection()

    sql = """
        SELECT DISTINCT
            tasks.*
        FROM tasks
    """

    values = []


    # Only join the tag tables when a label filter is actually being used.
    if tag_id:

        sql += """
            JOIN task_tags
                ON task_tags.task_id = tasks.id

            JOIN tags
                ON tags.id = task_tags.tag_id
        """


    # Never allow search results from another account.
    sql += """
        WHERE tasks.user_id = ?
    """

    values.append(
        user_id
    )


    # Search both title and description.
    # LOWER makes the search ignore uppercase and lowercase differences.
    if query:

        sql += """
            AND (
                LOWER(tasks.title)
                    LIKE LOWER(?)

                OR

                LOWER(
                    COALESCE(
                        tasks.description,
                        ''
                    )
                )
                    LIKE LOWER(?)
            )
        """

        search_text = (
            f"%{query}%"
        )

        values.extend([
            search_text,
            search_text
        ])


    if tag_id:

        sql += """
            AND tags.id = ?
            AND tags.user_id = ?
        """

        values.extend([
            tag_id,
            user_id
        ])


    if priority:

        sql += """
            AND tasks.priority = ?
        """

        values.append(
            priority
        )


    if state:

        sql += """
            AND tasks.state = ?
        """

        values.append(
            state
        )


    # Keep the newest matching tasks near the top.
    sql += """
        ORDER BY
            tasks.created_at DESC,
            tasks.id DESC
    """


    tasks = connection.execute(
        sql,
        values
    ).fetchall()

    connection.close()

    return tasks


# Get the task information needed for the Data page.
def get_task_statistics(user_id):

    connection = get_connection()

    tasks = connection.execute(
        """
        SELECT
            id,
            state,
            created_at,
            completed_at
        FROM tasks
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return tasks



# put any new database functions above this part


# create all the tables when CatOS first starts
# CREATE TABLE IF NOT EXISTS means existing tables will not be replaced
def create_tables():
    connection = get_connection()

    try:
        create_users_table(connection)
        create_tasks_table(connection)
        create_tags_table(connection)
        create_task_tags_table(connection)
        create_subtasks_table(connection)
        create_cat_table(connection)

        # save all table changes together
        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


# this only runs when database.py is run directly
# useful if I want to create/check the tables without starting the Flask app
if __name__ == "__main__":
    create_tables()