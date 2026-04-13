import os
import psycopg2
import psycopg2.extras
from constants import DEFAULT_CATEGORIES

DATABASE_URL = os.getenv("DATABASE_URL")
DEFAULT_CURRENCY = "UAH"
DEFAULT_NOTIFICATIONS = 1


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
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
            UNIQUE (name, user_id, is_default)
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
        cur.execute(
            "INSERT INTO categories (id, name, is_default) VALUES (gen_random_uuid()::text, %s, 1) ON CONFLICT DO NOTHING",
            (name,)
        )
    conn.commit()
    cur.close()
    conn.close()