import psycopg2.extras
from database import get_db


def get_weekly_breakdown(user_id: str, week_start: str, week_end: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT c.name as category, SUM(e.amount) as total
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = %s AND e.date BETWEEN %s AND %s
        GROUP BY e.category_id, c.name
    """, (user_id, week_start, week_end))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]


def get_monthly_breakdown(user_id: str, month: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT c.name as category, SUM(e.amount) as total
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = %s AND to_char(e.date::date, 'YYYY-MM') = %s
        GROUP BY e.category_id, c.name
    """, (user_id, month))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]


def get_small_purchases(user_id: str, week_start: str, categories: tuple):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    placeholders = ",".join(["%s"] * len(categories))
    cur.execute(f"""
        SELECT c.name as category, SUM(e.amount) as total, COUNT(*) as count
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = %s AND e.date >= %s AND c.name IN ({placeholders})
        GROUP BY e.category_id, c.name
    """, (user_id, week_start, *categories))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]