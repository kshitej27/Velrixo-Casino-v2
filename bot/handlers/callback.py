from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_callback_query(filters.regex("^games$"))
async def games_menu(_, query):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Dice", callback_data="dice")],
        [InlineKeyboardButton("🎯 Darts", callback_data="darts")],
        [InlineKeyboardButton("🎳 Bowling", callback_data="bowling")],
        [InlineKeyboardButton("🏐 Volleyball", callback_data="volley")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])
    await query.message.edit_text("🎮 Select a game to play:", reply_markup=keyboard)
