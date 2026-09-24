"""Create connections to the CatOS SQLite database."""

import sqlite3
from pathlib import Path


# connection.py is now inside the database folder,
# so go back one more folder to find CatOS.db.
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "CatOS.db"


def get_connection():
    """Open a connection to the CatOS SQLite database."""

    connection = sqlite3.connect(DATABASE_PATH)

    # Make the results easier to read.
    # For example, use user["username"] instead of user[1].
    connection.row_factory = sqlite3.Row

    # SQLite does not turn foreign keys on automatically.
    # This makes the relationships between the tables actually work.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
