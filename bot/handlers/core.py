# bot/handlers/core.py
from pyrogram import Client, filters
from bot.db import add_user, get_balance, get_last_daily, set_daily_time
from config import BOT_USERNAME, DAILY_REWARD, REFERRAL_BONUS
import time


@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    user = message.from_user
    args = message.text.split()

    ref = None
    if len(args) > 1 and args[1].isdigit():
        ref = int(args[1])

    is_new = add_user(user.id, user.username or "Unknown", ref)

    if is_new:
        text = (
            f"🎉 Welcome {user.mention} to *Velrixo Casino!* \n\n"
            f"🪙 You received **{DAILY_REWARD} coins** as a starting bonus!\n"
        )
        if ref:
            text += f"\n👥 Referral: {REFERRAL_BONUS} coins given to your inviter!"
    else:
        text = f"👋 Welcome back {user.mention}! Use /profile to view your balance."

    text += f"\n\n🔗 Invite & Earn:\n`https://t.me/{BOT_USERNAME}?start={user.id}`"

    await message.reply(text)


@Client.on_message(filters.command("profile"))
async def profile_handler(client, message):
    bal = get_balance(message.from_user.id)
    await message.reply(
        f"👤 *Your Profile*\n\n"
        f"🆔 ID: `{message.from_user.id}`\n"
        f"💰 Balance: `{bal}` coins\n\n"
        f"✅ Use /daily for free coins every 24h!"
    )


@Client.on_message(filters.command("daily"))
async def daily_handler(client, message):
    user_id = message.from_user.id
    last = get_last_daily(user_id)
    now = int(time.time())

    if now - last < 86400:  # 24h
        remaining = 86400 - (now - last)
        hours = remaining // 3600
        mins = (remaining % 3600) // 60
        return await message.reply(f"⏳ You already claimed! Come back in **{hours}h {mins}m**")

    from bot.db import update_balance
    update_balance(user_id, DAILY_REWARD)
    set_daily_time(user_id, now)

    await message.reply(f"✅ You received **{DAILY_REWARD} coins!**\nCome back tomorrow!")


@Client.on_message(filters.command("help"))
async def help_handler(client, message):
    await message.reply(
        "🎮 *Velrixo Casino Commands:*\n\n"
        "/start - Register & get bonus\n"
        "/profile - View coins\n"
        "/daily - Claim daily reward\n"
        "/slots - Play slot machine\n"
        "/help - Show this help menu"
    )
