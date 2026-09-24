"""Database functions used for CatOS user information."""

import sqlite3

from .connection import get_connection


def get_user_by_id(user_id):
    """Get one user from the database using their id."""

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


def update_user_avatar(user_id, avatar_url):
    """Save a new avatar path for one user."""

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
