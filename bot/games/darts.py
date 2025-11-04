# bot/games/darts.py
from pyrogram import Client, filters
from bot.db import get_balance, update_balance
import asyncio

@Client.on_message(filters.command("darts"))
async def darts_handler(client, message):
    user_id = message.from_user.id
    args = message.text.split()

    bet = 50
    if len(args) > 1 and args[1].isdigit():
        bet = int(args[1])

    balance = get_balance(user_id)
    if balance < bet:
        return await message.reply(f"❌ Not enough coins! You need at least {bet} coins.")

    update_balance(user_id, -bet)

    msg = await message.reply("🎯 Throwing dart...")
    await asyncio.sleep(1)

    dart_throw = await client.send_dice(message.chat.id, emoji="🎯")
    score = dart_throw.dice.value  # 1-6 (bullseye = 6)

    await asyncio.sleep(3)

    if score == 6:
        win = bet * 3
        update_balance(user_id, win)
        await message.reply(f"🎯 **BULLSEYE! (6)**\n✅ You win +{win} coins!")
    elif score >= 4:
        win = bet * 2
        update_balance(user_id, win)
        await message.reply(f"🎯 Hit **{score}**\n✅ You win +{win} coins!")
    else:
        await message.reply(f"🎯 Hit **{score}**\n😢 You lost {bet} coins.")

    bal = get_balance(user_id)
    await message.reply(f"💰 Current Balance: `{bal}` coins")
