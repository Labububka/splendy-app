import uuid
import psycopg2.extras
from database import get_db


def find_by_email(email: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return dict(user) if user else None


def find_by_email_and_password(email: str, password: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s", (email, password)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    return dict(user) if user else None


def find_by_id(user_id: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT id, email, name, currency, notifications FROM users WHERE id = %s", (user_id,)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def create(email: str, password: str, name: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    user_id = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO users (id, email, password, name) VALUES (%s, %s, %s, %s)",
        (user_id, email, password, name)
    )
    conn.commit()
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def update(user_id: str, fields: dict):
    conn = get_db()
    cur = conn.cursor()
    set_clause = ", ".join([f"{k} = %s" for k in fields])
    cur.execute(f"UPDATE users SET {set_clause} WHERE id = %s", (*fields.values(), user_id))
    conn.commit()
    cur.close()
    conn.close()