
# bot/games/slots.py
from pyrogram import Client, filters
from bot.db import get_balance, update_balance
import random
import asyncio

SLOT_EMOJIS = ["🍒", "🍋", "🍇", "🍉", "⭐", "🍀"]

@Client.on_message(filters.command("slots"))
async def slots_handler(client, message):
    user_id = message.from_user.id
    args = message.text.split()

    # default bet = 50 coins
    bet = 50
    if len(args) > 1 and args[1].isdigit():
        bet = int(args[1])

    balance = get_balance(user_id)
    if balance < bet:
        return await message.reply(f"❌ Not enough coins! You need at least {bet} coins.")

    # Deduct bet
    update_balance(user_id, -bet)

    # Send spinning animation
    msg = await message.reply("🎰 Spinning...")
    await asyncio.sleep(1)

    result = [random.choice(SLOT_EMOJIS) for _ in range(3)]
    await msg.edit(f"🎰 | {' | '.join(result)} |")

    # Check win
    if len(set(result)) == 1:  # Jackpot 🎉
        win = bet * 5
        update_balance(user_id, win)
        await msg.edit(f"🎰 | {' | '.join(result)} |\n\n🎉 JACKPOT! You win +{win} coins!")
    elif len(set(result)) == 2:  # Small win
        win = bet * 2
        update_balance(user_id, win)
        await msg.edit(f"🎰 | {' | '.join(result)} |\n\n✅ Nice! You win +{win} coins!")
    else:
        await msg.edit(f"🎰 | {' | '.join(result)} |\n\n😢 You lost {bet} coins... Better luck next time!")

    await asyncio.sleep(0.5)
    bal = get_balance(user_id)
    await msg.reply(f"💰 Current Balance: `{bal}` coins")
