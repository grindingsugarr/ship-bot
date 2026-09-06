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
    pass
