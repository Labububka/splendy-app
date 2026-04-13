import uuid
import psycopg2.extras
from database import get_db


def find_all_for_user(user_id: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT * FROM categories WHERE is_default = 1 OR user_id = %s", (user_id,)
    )
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(c) for c in categories]


def find_by_id(category_id: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
    category = cur.fetchone()
    cur.close()
    conn.close()
    return dict(category) if category else None


def find_by_id_and_user(category_id: str, user_id: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT * FROM categories WHERE id = %s AND user_id = %s AND is_default = 0",
        (category_id, user_id)
    )
    category = cur.fetchone()
    cur.close()
    conn.close()
    return dict(category) if category else None


def create(name: str, user_id: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    category_id = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO categories (id, name, user_id) VALUES (%s, %s, %s)",
        (category_id, name, user_id)
    )
    conn.commit()
    cur.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
    category = cur.fetchone()
    cur.close()
    conn.close()
    return dict(category)


def delete(category_id: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE id = %s", (category_id,))
    conn.commit()
    cur.close()
    conn.close()