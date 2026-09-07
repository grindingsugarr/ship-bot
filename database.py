import sqlite3
import os
from datetime import datetime

if os.path.exists("users.db"):
    os.remove("users.db")
    
conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()


# =========================
# USERS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    name TEXT,
    messages INTEGER DEFAULT 0,
    last_active TEXT
)
""")


# =========================
# SHIP HISTORY
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ship_history(
    user1 INTEGER,
    user2 INTEGER,
    compatibility INTEGER,
    times INTEGER DEFAULT 1,
    created_at TEXT
)
""")


conn.commit()


# =========================
# INTERACTION TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions(
    user1 INTEGER,
    user2 INTEGER,
    interactions INTEGER DEFAULT 1,
    last_interaction TEXT,
    UNIQUE(user1, user2)
)
""")

conn.commit()


# =========================
# UPDATE USER
# =========================

def update_user(chat_id, user):

    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO users(
        user_id,
        username,
        name,
        messages,
        last_active
    )

    VALUES(?,?,?,?,?)

    ON CONFLICT(user_id)

    DO UPDATE SET

        username = excluded.username,
        name = excluded.name,
        messages = messages + 1,
        last_active = excluded.last_active

    """,
    (
        user.id,
        user.username,
        user.full_name,
        1,
        now
    ))

    conn.commit()



# =========================
# GET USERS
# =========================

def get_users(chat_id=None):

    cursor.execute("""
SELECT
    user_id,
    username,
    name,
    messages,
    last_active
FROM users
""")

    return cursor.fetchall()



def save_interaction(user1, user2):

    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO interactions(
        user1,
        user2,
        interactions,
        last_interaction
    )

    VALUES(?,?,1,?)

    ON CONFLICT(user1,user2)

    DO UPDATE SET

    interactions = interactions + 1,
    last_interaction = excluded.last_interaction

    """,
    (
        user1,
        user2,
        now
    ))

    conn.commit()

# =========================
# SAVE SHIP RESULT
# =========================

def save_ship(user1, user2, compatibility):

    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO ship_history(
        user1,
        user2,
        compatibility,
        created_at
    )

    VALUES(?,?,?,?)

    """,
    (
        user1,
        user2,
        compatibility,
        now
    ))

    conn.commit()
