import sqlite3

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from database import get_connection


def register_user(username: str, password: str) -> bool:
    username = username.strip()

    if not username or not password:
        return False

    password_hash = generate_password_hash(password)

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        # 用户名已经存在
        return False

    finally:
        connection.close()


def login_user(username: str, password: str):
    username = username.strip()

    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, username, password_hash
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    if user is None:
        return None

    password_is_correct = check_password_hash(
        user["password_hash"],
        password
    )

    if not password_is_correct:
        return None

    return {
        "id": user["id"],
        "username": user["username"]
    }


# register logic

def register_user(username, password):
    username = username.strip()

    if not username or not password:
        return None

    password_hash = generate_password_hash(password)

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (
                username,
                password_hash
            )
            VALUES (?, ?)
            """,
            (username, password_hash),
        )

        connection.commit()

        user_id = cursor.lastrowid

        return {
            "id": user_id,
            "username": username,
        }

    except sqlite3.IntegrityError:
        # username 已经存在
        return None

    finally:
        connection.close()


def login_user(username, password):
    username = username.strip()

    connection = get_connection()

    user = connection.execute(
        """
        SELECT
            id,
            username,
            password_hash
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    connection.close()

    if user is None:
        return None

    if not check_password_hash(
        user["password_hash"],
        password,
    ):
        return None

    return {
        "id": user["id"],
        "username": user["username"],
    }