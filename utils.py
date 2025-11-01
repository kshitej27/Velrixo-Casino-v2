# utils.py
# Buttons, emoji animations & small helpers for Velrixo Casino Bot V2

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from random import choice

CURRENCY = "🪙"   # Chip symbol

# ---------- MAIN MENU ----------
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Games", callback_data="menu_games")],
        [InlineKeyboardButton(text=f"💰 Balance", callback_data="menu_balance")],
        [InlineKeyboardButton(text="🎁 Daily Reward", callback_data="menu_daily")],
        [InlineKeyboardButton(text="🎟 Redeem Code", callback_data="menu_redeem")],
        [InlineKeyboardButton(text="👑 Profile", callback_data="menu_profile")],
    ])
    return kb

# ---------- GAME MENU ----------
def games_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Dice", callback_data="game_dice")],
        [InlineKeyboardButton(text="🎰 Slot Machine", callback_data="game_slots")],
        [InlineKeyboardButton(text="🎯 Darts", callback_data="game_darts")],
        [InlineKeyboardButton(text="🏀 Basketball", callback_data="game_ball")],
        [InlineKeyboardButton(text="🎳 Bowling", callback_data="game_bowling")],
        [InlineKeyboardButton(text="⛔ Exit", callback_data="close_menu")],
    ])
    return kb

# ---------- CONFIRM KEYBOARD ----------
def confirm_kb(yes_data, no_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Yes", callback_data=yes_data),
         InlineKeyboardButton(text="❌ No", callback_data=no_data)]
    ])

# ---------- ANIMATED GAME EMOJIS ----------
DICE_FACES = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
SLOTS_SYMBOLS = ["🍒", "🍋", "💎", "7️⃣", "⭐", "🍉"]
DART_TARGET = ["🎯", "💥", "❌"]
BASKET = ["🏀", "💥", "❌"]
BOWLING = ["🎳", "💥", "❌"]

def spin_slots():
    return [choice(SLOTS_SYMBOLS) for _ in range(3)]

def dice_roll():
    return choice(DICE_FACES)

def animate_spin(frames=6):
    """Returns a list of slot spin frames for fake animation."""
    return [" ".join([choice(SLOTS_SYMBOLS) for _ in range(3)]) for _ in range(frames)]

def format_balance(amount: int):
    return f"{amount:,} {CURRENCY}"
