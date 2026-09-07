import sqlite3
from datetime import datetime


conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()


# ======================
# USER TABLE
# ======================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    name TEXT,
    messages INTEGER DEFAULT 0,
    last_active TEXT
)
""")


# ======================
# INTERACTION TABLE
# ======================

cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions(
    user1 INTEGER,
    user2 INTEGER,
    reply_count INTEGER DEFAULT 0,
    mention_count INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0,
    updated TEXT,

    PRIMARY KEY(user1,user2)
)
""")


# ======================
# SHIP HISTORY
# ======================

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



def update_user(user):

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

    username=?,
    name=?,
    messages=messages+1,
    last_active=?

    """,
    (
        user.id,
        user.username or "",
        user.full_name or "",
        1,
        now,

        user.username or "",
        user.full_name or "",
        now
    ))

    conn.commit()



def add_interaction(
    user1,
    user2,
    interaction_type="reply"
):

    if user1 == user2:
        return


    a,b = sorted(
        [user1,user2]
    )


    if interaction_type == "reply":

        cursor.execute("""
        INSERT INTO interactions(
            user1,
            user2,
            reply_count,
            score,
            updated
        )

        VALUES(?,?,?,?,?)

        ON CONFLICT(user1,user2)

        DO UPDATE SET

        reply_count=reply_count+1,
        score=score+3,
        updated=?

        """,
        (
            a,
            b,
            1,
            3,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))


    elif interaction_type == "mention":

        cursor.execute("""
        INSERT INTO interactions(
            user1,
            user2,
            mention_count,
            score,
            updated
        )

        VALUES(?,?,?,?,?)

        ON CONFLICT(user1,user2)

        DO UPDATE SET

        mention_count=mention_count+1,
        score=score+2,
        updated=?

        """,
        (
            a,
            b,
            1,
            2,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))


    conn.commit()



def get_users():

    cursor.execute("""
    SELECT
    user_id,
    username,
    name,
    messages

    FROM users
    """)

    return cursor.fetchall()



def get_interaction(
    user1,
    user2
):

    a,b = sorted(
        [user1,user2]
    )


    cursor.execute("""
    SELECT score
    FROM interactions

    WHERE user1=? AND user2=?

    """,
    (
        a,
        b
    ))


    result = cursor.fetchone()


    if result:
        return result[0]


    return 0
