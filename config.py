# config.py
import os

# Use env var BOT_TOKEN (recommended). If you temporarily want to embed, you can set it here,
# but DO NOT commit a real token to a public repo.
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Owner bot username (without @). Owner will be auto-added as admin when they /start
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Velrixo").lstrip("@")

# Sqlite DB filename
DB_FILE = os.getenv("DB_FILE", "velrixo_casino_v2.sqlite")

# Currency label
CURRENCY = os.getenv("CURRENCY", "$ Chips")

# Default referral bonus / small promo amounts
REF_BONUS_DEFAULT = int(os.getenv("REF_BONUS_DEFAULT", "500"))
DAILY_MIN = int(os.getenv("DAILY_MIN", "200"))
DAILY_MAX = int(os.getenv("DAILY_MAX", "500"))
