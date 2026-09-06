import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()


def get_users():
    cursor.execute("""
        SELECT user_id, username, name, messages
        FROM users
    """)

    return cursor.fetchall()


def update_user(user):
    cursor.execute("""
    INSERT INTO users(user_id, username, name, messages)
    VALUES (?, ?, ?, 1)
    ON CONFLICT(user_id)
    DO UPDATE SET
    messages = messages + 1
    """,
    (
        user.id,
        user.username or "",
        user.first_name
    ))

    conn.commit()
