from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.db import ensure_user

@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    user = message.from_user
    ensure_user(user.id, user.username)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Play Games", callback_data="games")],
        [InlineKeyboardButton("💰 Wallet", callback_data="wallet")],
        [InlineKeyboardButton("👥 Referral", callback_data="ref")],
        [InlineKeyboardButton("📊 Profile", callback_data="profile")]
    ])

    await message.reply(
        f"👋 Welcome to Velrixo Casino, {user.first_name}!\n"
        f"Play games and win coins 🎰",
        reply_markup=keyboard
    )
