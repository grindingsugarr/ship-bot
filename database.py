import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()


def get_users(chat_id=None):

    cursor.execute("""
        SELECT user_id, '', '', messages
        FROM users
    """)

    return cursor.fetchall()


def update_user(user_id, user):

    cursor.execute("""
    INSERT INTO users(user_id, messages)
    VALUES (?, 1)
    ON CONFLICT(user_id)
    DO UPDATE SET
    messages = messages + 1
    """,
    (
        user.id,
    ))

    conn.commit()
