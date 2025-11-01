# Velrixo Casino Bot V2

Telegram Casino bot (virtual currency `$ Chips`) using Aiogram 3.x + SQLite.

## Files
- `main.py` — entrypoint
- `config.py` — env vars and settings
- `database.py` — sqlite helpers
- `games.py` — game handlers (uses animated emojis)
- `admin.py` — admin commands
- `economy_handlers.py` — start/profile/redeem/daily/referral
- `utils.py` — buttons and helpers
- `requirements.txt`, `Procfile`

## Setup (local / Railway)
1. Set `BOT_TOKEN` environment variable (BotFather token).
2. `pip install -r requirements.txt`
3. `python main.py`
