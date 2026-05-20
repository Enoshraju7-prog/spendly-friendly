import sqlite3
from werkzeug.security import generate_password_hash


def get_db():
    conn = sqlite3.connect("spendly.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cur = conn.cursor()

    row = cur.execute("SELECT COUNT(*) FROM users").fetchone()
    if row[0] > 0:
        conn.close()
        return

    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cur.lastrowid

    sample_expenses = [
        (user_id, 32.50,  "Food",          "2026-05-01", "Grocery run"),
        (user_id, 18.00,  "Transport",     "2026-05-03", "Uber to office"),
        (user_id, 120.00, "Bills",         "2026-05-05", "Electricity bill"),
        (user_id, 45.00,  "Health",        "2026-05-08", "Pharmacy"),
        (user_id, 15.00,  "Entertainment", "2026-05-10", "Movie ticket"),
        (user_id, 60.00,  "Shopping",      "2026-05-12", "New shoes"),
        (user_id, 9.99,   "Other",         "2026-05-14", "Miscellaneous"),
        (user_id, 22.75,  "Food",          "2026-05-17", "Restaurant lunch"),
    ]
    cur.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )

    conn.commit()
    conn.close()
