import sqlite3
from datetime import datetime

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    chat_id INTEGER,
    user_id INTEGER,
    username TEXT,
    name TEXT,
    messages INTEGER DEFAULT 0,
    last_active TEXT,
    PRIMARY KEY(chat_id, user_id)
)
""")

conn.commit()


def update_user(chat_id, user):
    username = user.username or ""
    name = user.first_name or "Unknown"

    cursor.execute("""
    INSERT INTO users(
        chat_id,
        user_id,
        username,
        name,
        messages,
        last_active
    )
    VALUES (?, ?, ?, ?, ?, ?)

    ON CONFLICT(chat_id, user_id)
    DO UPDATE SET
        messages = messages + 1,
        last_active = ?
    """,
    (
        chat_id,
        user.id,
        username,
        name,
        1,
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))

    conn.commit()



def get_users(chat_id):

    cursor.execute("""
    SELECT user_id, username, name, messages
    FROM users
    WHERE chat_id = ?
    """,
    (chat_id,))

    return cursor.fetchall()
