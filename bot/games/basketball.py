
# basketball.py – Basketball Shoot 🏀

from aiogram import types
from aiogram.enums import ChatAction
from bot.db import get_balance, update_balance
from config import CURRENCY_LABEL

async def play_basketball(message: types.Message, bet: int):
    user_id = message.from_user.id
    balance = get_balance(user_id)

    if bet > balance:
        return await message.reply("❌ Not enough balance to shoot!")

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    sent = await message.answer_dice(emoji="🏀")
    score = sent.dice.value  # 1 to 6

    if score >= 4:
        payout = bet * 2
        update_balance(user_id, payout)
        await message.reply(f"🏀 Swish! You got a **{score}** and won {payout} {CURRENCY_LABEL} 🎉")
    else:
        update_balance(user_id, -bet)
        await message.reply(f"🏀 Missed! You got a **{score}** and lost {bet} {CURRENCY_LABEL} 💸")
