# config.py
# Velrixo Casino Bot V2 - configuration
# Keep secrets (BOT_TOKEN) in environment variables (Railway/Local .env), NOT in this file.

import os

# Bot token from @BotFather (set as env var in Railway: BOT_TOKEN)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Owner username (without @) - the owner will be auto-added as admin on first /start
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Velrixo").lstrip("@")

# Database filename (SQLite)
DB_FILE = os.getenv("DB_FILE", "velrixo_casino_v2.sqlite")

# Virtual currency label
CURRENCY_LABEL = os.getenv("CURRENCY_LABEL", "Chips")

# Default amounts (can change)
START_BALANCE = int(os.getenv("START_BALANCE", "1000"))
DAILY_MIN = int(os.getenv("DAILY_MIN", "400"))
DAILY_MAX = int(os.getenv("DAILY_MAX", "600"))
REFERRAL_BONUS = int(os.getenv("REFERRAL_BONUS", "200"))

# Misc
MAX_BET_PERCENT = float(os.getenv("MAX_BET_PERCENT", "0.10"))  # max bet = 10% of balance
