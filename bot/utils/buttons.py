
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Main Menu
def main_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎮 Games", callback_data="games")],
            [InlineKeyboardButton("💰 Wallet", callback_data="wallet")],
            [InlineKeyboardButton("🆘 Help", callback_data="help")]
        ]
    )

# Games Menu
def games_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎲 Dice", callback_data="dice")],
            [InlineKeyboardButton("🎯 Darts", callback_data="darts")],
            [InlineKeyboardButton("🎰 Slots", callback_data="slots")],
            [InlineKeyboardButton("⚽ Football", callback_data="football")],
            [InlineKeyboardButton("🎳 Bowling", callback_data="bowling")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu")]
        ]
    )

# Wallet Menu
def wallet_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💸 Check Balance", callback_data="balance")],
            [InlineKeyboardButton("🎁 Daily Bonus", callback_data="daily")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu")]
        ]
    )
