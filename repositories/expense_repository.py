import uuid
from database import get_db


def find_all(user_id: str, date_from=None, date_to=None, category_id=None):
    db = get_db()
    query = """
        SELECT e.*, c.name as category_name
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = ?
    """
    params = [user_id]
    if date_from:
        query += " AND e.date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND e.date <= ?"
        params.append(date_to)
    if category_id:
        query += " AND e.category_id = ?"
        params.append(category_id)
    query += " ORDER BY e.date DESC"
    expenses = db.execute(query, params).fetchall()
    db.close()
    return [dict(e) for e in expenses]


def find_by_id(expense_id: str):
    db = get_db()
    expense = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    db.close()
    return dict(expense) if expense else None


def find_by_id_and_user(expense_id: str, user_id: str):
    db = get_db()
    expense = db.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id)
    ).fetchone()
    db.close()
    return dict(expense) if expense else None


def create(user_id: str, amount: float, category_id: str, note: str, date: str):
    db = get_db()
    expense_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO expenses (id, user_id, amount, category_id, note, date) VALUES (?, ?, ?, ?, ?, ?)",
        (expense_id, user_id, amount, category_id, note, date)
    )
    db.commit()
    expense = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    db.close()
    return dict(expense)


def update(expense_id: str, fields: dict):
    db = get_db()
    set_clause = ", ".join([f"{k} = ?" for k in fields])
    db.execute(f"UPDATE expenses SET {set_clause} WHERE id = ?", (*fields.values(), expense_id))
    db.commit()
    db.close()


def delete(expense_id: str):
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    db.commit()
    db.close()
