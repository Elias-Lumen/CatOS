import sqlite3

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

# use the same database connection from database.py
# so I do not need to write the SQLite connection again here
from database import get_connection


# create a new user account
def register_user(username, password):

    # remove spaces before and after the username
    # but spaces inside the username are still kept
    username = username.strip()

    # both username and password are required
    if not username or not password:
        return None

    # never save the real password into the database
    # save the hashed version instead
    password_hash = generate_password_hash(password)

    connection = get_connection()

    try:
        # add the new user into the users table
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

        # save the new account
        connection.commit()

        # get the id SQLite just made for this user
        # this lets CatOS log them in straight after registration
        user_id = cursor.lastrowid

        # send the new user's information back to app.py
        return {
            "id": user_id,
            "username": username,
        }

    except sqlite3.IntegrityError:
        # username is UNIQUE in the database
        # so this normally means someone already has this username
        return None

    finally:
        # always close the database connection
        connection.close()


# check the username and password when a user logs in
def login_user(username, password):

    # remove accidental spaces before or after the username
    username = username.strip()

    connection = get_connection()

    # look for an account with this username
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

    # no account was found with that username
    if user is None:
        return None

    # compare the password with the saved password hash
    # if they do not match, the login should fail
    if not check_password_hash(
        user["password_hash"],
        password,
    ):
        return None

    # login worked, so return the information app.py needs
    # the password hash does not need to leave this function
    return {
        "id": user["id"],
        "username": user["username"],
    }