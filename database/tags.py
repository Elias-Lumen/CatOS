"""Database functions used for CatOS labels and task-label relationships."""

import sqlite3

from .connection import get_connection


def create_tag(user_id, name):
    """Create a label for one user, or reuse it if it already exists."""

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

        # Do not make a duplicate if this label already exists.
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


def get_tags_by_user(user_id):
    """Get all labels that belong to one user."""

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


def get_tasks_by_tag(
    user_id,
    tag_id
):
    """Get the tasks connected to one label for this user."""

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


def update_tag(
    tag_id,
    user_id,
    name
):
    """Change the name of one label."""

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


def delete_tag(
    tag_id,
    user_id
):
    """Delete one label without deleting the tasks that used it."""

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


def get_tags_by_task(task_id, user_id):
    """Get all labels attached to one task."""

    connection = get_connection()

    # Joining tasks here also checks that the task
    # actually belongs to the current user.
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


def set_task_tags(task_id, user_id, tag_ids):
    """Replace all labels attached to one task."""

    connection = get_connection()

    try:
        # Check that the task really belongs to this user first.
        # Otherwise changing the task id could affect someone else's task.
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

        # Remove the old relationships before adding the new ones.
        connection.execute(
            """
            DELETE FROM task_tags
            WHERE task_id = ?
            """,
            (task_id,)
        )

        for tag_id in tag_ids:

            # Only use labels that belong to this user.
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
