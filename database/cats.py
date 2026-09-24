"""Database functions used for the CatOS virtual cat."""

import sqlite3

from .connection import get_connection


def get_cat_by_user(user_id):
    """Get one user's virtual cat."""

    connection = get_connection()

    cat = connection.execute(
        """
        SELECT *
        FROM cat
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return cat


def create_cat_for_user(
    user_id,
    cat_name="Cat"
):
    """Create a cat if this user does not have one yet."""

    connection = get_connection()

    try:
        # Check first because each user should only have one cat.
        existing_cat = connection.execute(
            """
            SELECT id
            FROM cat
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        if existing_cat:
            return existing_cat["id"]

        cursor = connection.execute(
            """
            INSERT INTO cat (
                user_id,
                cat_name
            )
            VALUES (?, ?)
            """,
            (
                user_id,
                cat_name
            )
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def rename_cat(
    user_id,
    cat_name
):
    """Change the current user's cat name."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE cat
            SET
                cat_name = ?,
                last_interaction = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (
                cat_name,
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


def reward_cat_for_task(user_id):
    """Make the cat happier when its user finishes a task."""

    connection = get_connection()

    try:
        # Mood goes up by 5,
        # but it is never allowed to go above 100.
        connection.execute(
            """
            UPDATE cat
            SET
                mood = MIN(
                    mood + 5,
                    100
                ),
                last_interaction = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (user_id,)
        )

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()
