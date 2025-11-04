# bowling.py – Bowling Game 🎳

from aiogram import types
from aiogram.enums import ChatAction
from bot.db import get_balance, update_balance
from config import CURRENCY_LABEL

async def play_bowling(message: types.Message, bet: int):
    user_id = message.from_user.id
    balance = get_balance(user_id)

    if bet > balance:
        return await message.reply("❌ Not enough balance to play bowling!")

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    sent = await message.answer_dice(emoji="🎳")
    score = sent.dice.value  # 1 to 6

    if score == 6:
        payout = bet * 3
    elif score == 5:
        payout = bet * 2
    elif score >= 3:
        payout = bet
    else:
        payout = -bet

    update_balance(user_id, payout)

    if payout > 0:
        await message.reply(f"🎳 You knocked **{score} pins** and won {payout} {CURRENCY_LABEL}! 🎉")
    else:
        await message.reply(f"🎳 Only **{score} pins**... You lost {bet} {CURRENCY_LABEL}! 💸")
