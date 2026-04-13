import uuid
from database import get_db


def find_by_email(email: str):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    db.close()
    return user


def find_by_email_and_password(email: str, password: str):
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
    ).fetchone()
    db.close()
    return user


def find_by_id(user_id: str):
    db = get_db()
    user = db.execute(
        "SELECT id, email, name, currency, notifications FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    db.close()
    return user


def create(email: str, password: str, name: str):
    db = get_db()
    user_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO users (id, email, password, name) VALUES (?, ?, ?, ?)",
        (user_id, email, password, name)
    )
    db.commit()
    user = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    db.close()
    return user


def update(user_id: str, fields: dict):
    db = get_db()
    set_clause = ", ".join([f"{k} = ?" for k in fields])
    db.execute(f"UPDATE users SET {set_clause} WHERE id = ?", (*fields.values(), user_id))
    db.commit()
    db.close()
