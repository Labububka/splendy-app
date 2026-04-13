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
    default_categories_sql = ", ".join(
        [f"('{name}', 1)" for name in DEFAULT_CATEGORIES]
    )
    db.executescript(f"""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            currency TEXT DEFAULT '{DEFAULT_CURRENCY}',
            notifications INTEGER DEFAULT {DEFAULT_NOTIFICATIONS}
        );
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER,
            is_default INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER,
            note TEXT,
            date TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
        INSERT OR IGNORE INTO categories (name, is_default) VALUES {default_categories_sql};
    """)
    db.commit()
    db.close()
