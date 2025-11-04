# coinflip.py – Coin Flip 🪙

from aiogram import types
from random import choice
from bot.db import get_balance, update_balance
from config import CURRENCY_LABEL

async def play_coinflip(message: types.Message, bet: int, guess: str):
    user_id = message.from_user.id
    balance = get_balance(user_id)

    if bet > balance:
        return await message.reply("❌ Not enough balance to flip the coin!")

    result = choice(["heads", "tails"])

    if guess == result:
        payout = bet
        update_balance(user_id, payout)
        await message.reply(f"🪙 It's **{result}**! You won {payout} {CURRENCY_LABEL}! 🎉")
    else:
        update_balance(user_id, -bet)
        await message.reply(f"🪙 It's **{result}**! You lost {bet} {CURRENCY_LABEL}! 💸")
