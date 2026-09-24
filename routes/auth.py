"""Handle the database work for registering and logging in users."""

import sqlite3

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

# Use the same database connection from database.py
# so I do not need to write the SQLite connection again here.
from database import get_connection


def register_user(username, password):
    """Create a new user account with a hashed password."""

    # Remove spaces before and after the username,
    # but spaces inside the username are still kept.
    username = username.strip()

    # Both username and password are required.
    if not username or not password:
        return None

    # Never save the real password into the database.
    # Save the hashed version instead.
    password_hash = generate_password_hash(password)

    connection = get_connection()

    try:
        # Add the new user into the users table.
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

        # Save the new account.
        connection.commit()

        # Get the id SQLite just made for this user.
        # This lets CatOS log them in straight after registration.
        user_id = cursor.lastrowid

        # Send the new user's information back.
        return {
            "id": user_id,
            "username": username,
        }

    except sqlite3.IntegrityError:
        # Username is UNIQUE in the database,
        # so this normally means someone already has this username.
        return None

    finally:
        # Always close the database connection.
        connection.close()


def login_user(username, password):
    """Check the username and password and return the user if they match."""

    # Remove accidental spaces before or after the username.
    username = username.strip()

    connection = get_connection()

    # Look for an account with this username.
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

    # No account was found with that username.
    if user is None:
        return None

    # Compare the password with the saved password hash.
    # If they do not match, the login should fail.
    if not check_password_hash(
        user["password_hash"],
        password,
    ):
        return None

    # Login worked, so only return the information CatOS needs.
    # The password hash does not need to leave this function.
    return {
        "id": user["id"],
        "username": user["username"],
    }
