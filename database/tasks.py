"""Database functions used for main CatOS tasks."""

import sqlite3

from .connection import get_connection


def create_task(
    user_id,
    title,
    description=None,
    state="not_started",
    priority="normal",
    start_date=None,
    due_date=None
):
    """Create a new task and return its id."""

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


def get_tasks_by_user(user_id):
    """Get one user's tasks in the order they should be displayed."""

    connection = get_connection()

    # Completed tasks go lower because unfinished ones
    # are more useful to see first.
    # Then sort them by priority and creation time.
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
    """Switch a task between completed and not started."""

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

        # Do nothing if this task does not belong to the current user.
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
    """Save edited information for one task."""

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

def reschedule_overdue_tasks(
    user_id,
    today,
    new_due_date
):
    """Move all unfinished overdue tasks to one new due date."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE tasks
            SET due_date = ?
            WHERE user_id = ?
              AND due_date IS NOT NULL
              AND due_date < ?
              AND state != 'completed'
            """,
            (
                new_due_date,
                user_id,
                today
            )
        )

        connection.commit()

        return cursor.rowcount

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()

def delete_task(task_id, user_id):
    """Delete one task that belongs to the current user."""

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


def search_tasks(
    user_id,
    query="",
    tag_id=None,
    priority=None,
    state=None
):
    """Search one user's tasks using any filters that were provided."""

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


def get_task_statistics(user_id):
    """Get the task information needed by the Data page."""

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


def get_task_state(
    task_id,
    user_id
):
    """Get the current state of one task."""

    connection = get_connection()

    task = connection.execute(
        """
        SELECT state
        FROM tasks
        WHERE
            id = ?
            AND user_id = ?
        """,
        (
            task_id,
            user_id
        )
    ).fetchone()

    connection.close()

    if task is None:
        return None

    return task["state"]
