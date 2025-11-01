# database.py
import sqlite3
import random
from datetime import datetime
from config import DB_FILE, REF_BONUS_DEFAULT

_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
_cur = _conn.cursor()

def init_db():
    _cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY,
      username TEXT,
      balance INTEGER DEFAULT 1000,
      xp INTEGER DEFAULT 0,
      level INTEGER DEFAULT 1,
      last_daily TEXT DEFAULT '',
      streak INTEGER DEFAULT 0,
      ref_code TEXT,
      referred_by TEXT
    )""")
    _cur.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
    _cur.execute("""
    CREATE TABLE IF NOT EXISTS redeem_codes (
      code TEXT PRIMARY KEY,
      amount INTEGER,
      uses_allowed INTEGER DEFAULT 1,
      uses_count INTEGER DEFAULT 0,
      creator_id INTEGER,
      created_at TEXT
    )""")
    _cur.execute("""
    CREATE TABLE IF NOT EXISTS used_codes (
      code TEXT,
      user_id INTEGER,
      used_at TEXT,
      PRIMARY KEY(code,user_id)
    )""")
    _cur.execute("""
    CREATE TABLE IF NOT EXISTS packets (
      user_id INTEGER PRIMARY KEY,
      amount INTEGER DEFAULT 0,
      last_redeem TEXT DEFAULT ''
    )""")
    _conn.commit()

# ------------------ user helpers ------------------
def ensure_user(user_id: int, username: str | None = None) -> str:
    _cur.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,))
    if not _cur.fetchone():
        code = f"VCB{random.randint(10000,99999)}"
        _cur.execute("INSERT INTO users(user_id, username, balance, xp, level, last_daily, streak, ref_code) VALUES (?,?,?,?,?,?,?,?)",
                     (user_id, username or "", 1000, 0, 1, "", 0, code))
        _conn.commit()
        # create a small default redeem code for new user (optional promo)
        _cur.execute("INSERT OR IGNORE INTO redeem_codes(code,amount,uses_allowed,uses_count,creator_id,created_at) VALUES (?,?,?,?,?,?)",
                     (code, REF_BONUS_DEFAULT, 0, 0, user_id, datetime.utcnow().isoformat()))
        _conn.commit()
        return code
    else:
        if username:
            _cur.execute("UPDATE users SET username=? WHERE user_id=?", (username, user_id))
            _conn.commit()
    return ""

def get_user_row(user_id: int):
    _cur.execute("SELECT user_id, username, balance, xp, level, last_daily, streak, ref_code, referred_by FROM users WHERE user_id=?", (user_id,))
    return _cur.fetchone()

def get_balance(user_id: int) -> int:
    row = get_user_row(user_id)
    if row:
        return row[2]
    ensure_user(user_id)
    return 1000

def change_balance(user_id:int, delta:int) -> int:
    ensure_user(user_id)
    bal = get_balance(user_id)
    new = bal + int(delta)
    if new < 0:
        new = 0
    _cur.execute("UPDATE users SET balance=? WHERE user_id=?", (new, user_id))
    _conn.commit()
    return new

def set_balance(user_id:int, amount:int):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET balance=? WHERE user_id=?", (int(amount), user_id))
    _conn.commit()

def add_xp(user_id:int, xp:int):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET xp = xp + ? WHERE user_id=?", (xp, user_id))
    _conn.commit()
    _cur.execute("SELECT xp, level FROM users WHERE user_id=?", (user_id,))
    row = _cur.fetchone()
    if row:
        xp_now, level = row
        while xp_now >= level * 100:
            level += 1
            _cur.execute("UPDATE users SET level=? WHERE user_id=?", (level, user_id))
            _conn.commit()

# ------------------ admin helpers ------------------
def is_admin(user_id:int) -> bool:
    _cur.execute("SELECT 1 FROM admins WHERE user_id=?", (user_id,))
    return bool(_cur.fetchone())

def add_admin(user_id:int):
    _cur.execute("INSERT OR IGNORE INTO admins(user_id) VALUES (?)", (user_id,))
    _conn.commit()

def remove_admin(user_id:int):
    _cur.execute("DELETE FROM admins WHERE user_id=?", (user_id,))
    _conn.commit()

# ------------------ redeem codes ------------------
def make_code(code:str, amount:int, uses_allowed:int, creator_id:int):
    now = datetime.utcnow().isoformat()
    _cur.execute("INSERT OR REPLACE INTO redeem_codes(code,amount,uses_allowed,uses_count,creator_id,created_at) VALUES (?,?,?,?,?,?)",
                 (code, int(amount), int(uses_allowed), 0, creator_id, now))
    _conn.commit()

def get_code_row(code:str):
    _cur.execute("SELECT code, amount, uses_allowed, uses_count, creator_id FROM redeem_codes WHERE code=?", (code,))
    return _cur.fetchone()

def mark_code_used(code:str, user_id:int):
    now = datetime.utcnow().isoformat()
    _cur.execute("INSERT OR IGNORE INTO used_codes(code,user_id,used_at) VALUES (?,?,?)", (code, user_id, now))
    _cur.execute("UPDATE redeem_codes SET uses_count = uses_count + 1 WHERE code=?", (code,))
    _conn.commit()

def user_used_code(code:str, user_id:int) -> bool:
    _cur.execute("SELECT 1 FROM used_codes WHERE code=? AND user_id=?", (code, user_id))
    return bool(_cur.fetchone())

# ------------------ packets ------------------
def give_packet(user_id:int, amount:int):
    _cur.execute("INSERT OR REPLACE INTO packets(user_id,amount,last_redeem) VALUES (?,?, COALESCE((SELECT last_redeem FROM packets WHERE user_id=?), ''))",
                 (user_id, amount, user_id))
    _conn.commit()

def get_packet(user_id:int):
    _cur.execute("SELECT amount, last_redeem FROM packets WHERE user_id=?", (user_id,))
    return _cur.fetchone()

def set_packet_redeemed(user_id:int):
    _cur.execute("UPDATE packets SET last_redeem=? WHERE user_id=?", (datetime.utcnow().isoformat(), user_id))
    _conn.commit()

def top_players(limit=10):
    _cur.execute("SELECT username, balance FROM users ORDER BY balance DESC LIMIT ?", (limit,))
    return _cur.fetchall()
