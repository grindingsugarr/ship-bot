import sqlite3
from datetime import datetime

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    name TEXT,
    messages INTEGER DEFAULT 0,
    last_active TEXT
)
""")

conn.commit()


def update_user(user):
    username = user.username or ""
    name = user.first_name

    cursor.execute("""
    INSERT INTO users(user_id, username, name, messages, last_active)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(user_id)
    DO UPDATE SET
    messages = messages + 1,
    last_active = ?
    """,
    (
        user.id,
        username,
        name,
        1,
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))

    conn.commit()


def get_users():
    cursor.execute("""
    SELECT user_id, username, name, messages
    FROM users
    """)

    return cursor.fetchall()