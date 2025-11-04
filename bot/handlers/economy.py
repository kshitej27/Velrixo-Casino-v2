from pyrogram import Client, filters
from bot.db import get_coins, update_coins

@Client.on_callback_query(filters.regex("^wallet$"))
async def wallet_handler(_, query):
    user_id = query.from_user.id
    balance = get_coins(user_id)

    await query.message.edit_text(
        f"💰 Your balance: {balance} 💵\n\n"
        "🎁 Free daily reward: /daily\n"
        "🤑 Earn by playing games!",
        reply_markup=query.message.reply_markup
    )
