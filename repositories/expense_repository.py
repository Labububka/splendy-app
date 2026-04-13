import uuid
import psycopg2.extras
from database import get_db


def find_all(user_id: str, date_from=None, date_to=None, category_id=None):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT e.*, c.name as category_name
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = %s
    """
    params = [user_id]
    if date_from:
        query += " AND e.date >= %s"
        params.append(date_from)
    if date_to:
        query += " AND e.date <= %s"
        params.append(date_to)
    if category_id:
        query += " AND e.category_id = %s"
        params.append(category_id)
    query += " ORDER BY e.date DESC"
    cur.execute(query, params)
    expenses = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(e) for e in expenses]


def find_by_id(expense_id: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM expenses WHERE id = %s", (expense_id,))
    expense = cur.fetchone()
    cur.close()
    conn.close()
    return dict(expense) if expense else None


def find_by_id_and_user(expense_id: str, user_id: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT * FROM expenses WHERE id = %s AND user_id = %s", (expense_id, user_id)
    )
    expense = cur.fetchone()
    cur.close()
    conn.close()
    return dict(expense) if expense else None


def create(user_id: str, amount: float, category_id: str, note: str, date: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    expense_id = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO expenses (id, user_id, amount, category_id, note, date) VALUES (%s, %s, %s, %s, %s, %s)",
        (expense_id, user_id, amount, category_id, note, date)
    )
    conn.commit()
    cur.execute("SELECT * FROM expenses WHERE id = %s", (expense_id,))
    expense = cur.fetchone()
    cur.close()
    conn.close()
    return dict(expense)


def update(expense_id: str, fields: dict):
    conn = get_db()
    cur = conn.cursor()
    set_clause = ", ".join([f"{k} = %s" for k in fields])
    cur.execute(f"UPDATE expenses SET {set_clause} WHERE id = %s", (*fields.values(), expense_id))
    conn.commit()
    cur.close()
    conn.close()


def delete(expense_id: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    cur.close()
    conn.close()