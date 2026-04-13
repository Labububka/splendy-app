import sqlite3
from constants import DEFAULT_CATEGORIES

DATABASE_NAME = "splendy.db"
DEFAULT_CURRENCY = "UAH"
DEFAULT_NOTIFICATIONS = 1


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    db.executescript(f"""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            currency TEXT DEFAULT '{DEFAULT_CURRENCY}',
            notifications INTEGER DEFAULT {DEFAULT_NOTIFICATIONS}
        );
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            user_id TEXT,
            is_default INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            CONSTRAINT unique_category UNIQUE (name, user_id, is_default)
        );
        CREATE TABLE IF NOT EXISTS expenses (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id TEXT,
            note TEXT,
            date TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
    """)
    for name in DEFAULT_CATEGORIES:
        db.execute(
            "INSERT OR IGNORE INTO categories (id, name, is_default) VALUES (lower(hex(randomblob(16))), ?, 1)",
            (name,)
        )
    db.commit()
    db.close()