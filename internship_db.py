import sqlite3
from datetime import datetime

DATABASE = "internship_agent.db"

ACTION_WEIGHTS = {
    "search": 1,
    "view": 2,
    "click": 3,
    "save": 5,
    "apply": 7
}


def get_connection():
    return sqlite3.connect(DATABASE)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            action TEXT NOT NULL,
            internship_id TEXT,
            internship_title TEXT,
            company TEXT,
            skills TEXT,
            role TEXT,
            location TEXT,
            search_keyword TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_interests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            interest TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            updated_at TEXT,
            UNIQUE(user_id, interest)
        )
    """)

    conn.commit()
    conn.close()


def record_interaction(
    user_id,
    action,
    internship_id="",
    internship_title="",
    company="",
    skills="",
    role="",
    location="",
    search_keyword=""
):
    if action not in ACTION_WEIGHTS:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interactions (
            user_id,
            action,
            internship_id,
            internship_title,
            company,
            skills,
            role,
            location,
            search_keyword,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        action,
        internship_id,
        internship_title,
        company,
        skills,
        role,
        location,
        search_keyword,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

    update_user_interests(
        user_id,
        action,
        internship_title,
        company,
        skills,
        role,
        search_keyword
    )


def update_user_interests(
    user_id,
    action,
    internship_title="",
    company="",
    skills="",
    role="",
    search_keyword=""
):
    weight = ACTION_WEIGHTS.get(action, 0)

    interests = []

    if skills:
        if isinstance(skills, list):
            interests.extend(skills)
        else:
            interests.extend(
                str(skills).replace(";", ",").split(",")
            )

    if role:
        interests.append(role)

    if search_keyword:
        interests.append(search_keyword)

    if internship_title:
        interests.append(internship_title)

    for interest in interests:

        interest = str(interest).strip().lower()

        if not interest:
            continue

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO user_interests
                (user_id, interest, score, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, interest)
            DO UPDATE SET
                score = score + excluded.score,
                updated_at = excluded.updated_at
        """, (
            user_id,
            interest,
            weight,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()


def get_user_interests(user_id, limit=20):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT interest, score, updated_at
        FROM user_interests
        WHERE user_id = ?
        ORDER BY score DESC
        LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "interest": row[0],
            "score": row[1],
            "updated_at": row[2]
        }
        for row in rows
    ]


def get_recent_interactions(user_id, limit=20):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            action,
            internship_id,
            internship_title,
            company,
            skills,
            role,
            location,
            search_keyword,
            created_at
        FROM interactions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "action": row[0],
            "internship_id": row[1],
            "internship_title": row[2],
            "company": row[3],
            "skills": row[4],
            "role": row[5],
            "location": row[6],
            "search_keyword": row[7],
            "created_at": row[8]
        }
        for row in rows
    ]


initialize_database()