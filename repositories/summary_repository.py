from database import get_db


def get_weekly_breakdown(user_id: str, week_start: str, week_end: str):
    db = get_db()
    rows = db.execute("""
        SELECT c.name as category, SUM(e.amount) as total
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = ? AND e.date BETWEEN ? AND ?
        GROUP BY e.category_id
    """, (user_id, week_start, week_end)).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_monthly_breakdown(user_id: str, month: str):
    db = get_db()
    rows = db.execute("""
        SELECT c.name as category, SUM(e.amount) as total
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = ? AND strftime('%Y-%m', e.date) = ?
        GROUP BY e.category_id
    """, (user_id, month)).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_small_purchases(user_id: str, week_start: str, categories: tuple):
    db = get_db()
    placeholders = ",".join("?" * len(categories))
    rows = db.execute(f"""
        SELECT c.name as category, SUM(e.amount) as total, COUNT(*) as count
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = ? AND e.date >= ? AND c.name IN ({placeholders})
        GROUP BY e.category_id
    """, (user_id, week_start, *categories)).fetchall()
    db.close()
    return [dict(r) for r in rows]