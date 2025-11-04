# bot/db.py
# SQLite Database for Velrixo Casino Bot V2

import sqlite3
from config import DB_FILE, START_BALANCE, REFERRAL_BONUS


def connect():
    """Connect to SQLite database."""
    return sqlite3.connect(DB_FILE)


def init_db():
    """Create tables if they do not exist."""
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 0,
                last_daily INTEGER DEFAULT 0,
                referred_by INTEGER DEFAULT NULL
            )
        """)
        db.commit()


def add_user(user_id: int, username: str, ref: int = None):
    """Register user if not exists, give starting balance and referral bonus."""
    with connect() as db:
        existing = db.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if existing:
            return False  # user already exists

        db.execute(
            "INSERT INTO users (user_id, username, balance, referred_by) VALUES (?, ?, ?, ?)",
            (user_id, username, START_BALANCE, ref)
        )

        # Add referral bonus if valid referral & not self-referral
        if ref and ref != user_id:
            db.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (REFERRAL_BONUS, ref)
            )

        db.commit()
        return True


def get_balance(user_id: int) -> int:
    with connect() as db:
        res = db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return res[0] if res else 0


def update_balance(user_id: int, amount: int):
    with connect() as db:
        db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        db.commit()


def set_daily_time(user_id: int, timestamp: int):
    with connect() as db:
        db.execute("UPDATE users SET last_daily = ? WHERE user_id = ?", (timestamp, user_id))
        db.commit()


def get_last_daily(user_id: int) -> int:
    with connect() as db:
        res = db.execute("SELECT last_daily FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return res[0] if res else 0
