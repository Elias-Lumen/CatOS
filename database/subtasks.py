"""Database functions used for CatOS subtasks."""

import sqlite3

from .connection import get_connection


def create_subtask(
    task_id,
    user_id,
    title,
    description=None,
    priority="normal",
    due_date=None
):
    """Create a subtask under one of the current user's tasks."""

    connection = get_connection()

    try:
        # Check the main task first so a subtask cannot
        # be added to another user's task.
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


def get_subtasks_by_task(task_id, user_id):
    """Get all subtasks under one of the current user's tasks."""

    connection = get_connection()

    # Joining the main task lets user_id protect
    # subtasks from being read by another account.
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


def toggle_subtask_completion(
    subtask_id,
    user_id
):
    """Switch a subtask between completed and not started."""

    connection = get_connection()

    try:
        # Check through the main task so this user
        # cannot change another user's subtask.
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


def update_subtask(
    subtask_id,
    user_id,
    title,
    description=None,
    priority="normal",
    due_date=None
):
    """Save edited information for one subtask."""

    connection = get_connection()

    try:
        # The inner query checks ownership through the main task.
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


def delete_subtask(
    subtask_id,
    user_id
):
    """Delete one subtask belonging to the current user."""

    connection = get_connection()

    try:
        # Again check ownership through the main task before deleting.
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
