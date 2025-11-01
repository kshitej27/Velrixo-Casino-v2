# utils.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import CURRENCY

def flashy_welcome_kb(balance_text: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Enter Casino", callback_data="menu:games")],
        [InlineKeyboardButton(text=f"💰 {balance_text}", callback_data="menu:wallet")],
        [
            InlineKeyboardButton(text="🎮 Play Games", callback_data="menu:games"),
            InlineKeyboardButton(text="🔗 Referral", callback_data="menu:referral")
        ],
        [InlineKeyboardButton(text="🆘 Help", callback_data="menu:help")]
    ])
    return kb

def main_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Games", callback_data="menu:games")],
        [InlineKeyboardButton(text="💰 Wallet", callback_data="menu:wallet"),
         InlineKeyboardButton(text="🏆 Leaderboard", callback_data="menu:leaderboard")],
        [InlineKeyboardButton(text="🔗 Referral", callback_data="menu:referral")]
    ])
    return kb

def games_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🎰 Slots", callback_data="game:slots"),
         InlineKeyboardButton("🎲 Dice", callback_data="game:dice")],
        [InlineKeyboardButton("🎯 Dart", callback_data="game:dart"),
         InlineKeyboardButton("🚀 Crash", callback_data="game:crash")],
        [InlineKeyboardButton("🎳 Bowling", callback_data="game:bowl"),
         InlineKeyboardButton("💣 Mines", callback_data="game:mines")],
        [InlineKeyboardButton("🐉 DragonTiger", callback_data="game:dragontiger")],
        [InlineKeyboardButton("⬅️ Back", callback_data="menu:back")]
    ])
    return kb

def fmt_amount(amount:int) -> str:
    return f"{amount} {CURRENCY}"

def username_or_name(user):
    return user.username or user.first_name or str(user.id)
