from database import get_db


def find_all_for_user(user_id: int):
    db = get_db()
    categories = db.execute(
        "SELECT * FROM categories WHERE is_default = 1 OR user_id = ?", (user_id,)
    ).fetchall()
    db.close()
    return [dict(c) for c in categories]


def find_by_id_and_user(category_id: int, user_id: int):
    db = get_db()
    category = db.execute(
        "SELECT * FROM categories WHERE id = ? AND user_id = ? AND is_default = 0",
        (category_id, user_id)
    ).fetchone()
    db.close()
    return dict(category) if category else None


def create(name: str, user_id: int):
    db = get_db()
    cursor = db.execute("INSERT INTO categories (name, user_id) VALUES (?, ?)", (name, user_id))
    db.commit()
    category = db.execute("SELECT * FROM categories WHERE id = ?", (cursor.lastrowid,)).fetchone()
    db.close()
    return dict(category)


def delete(category_id: int):
    db = get_db()
    db.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    db.commit()
    db.close()
