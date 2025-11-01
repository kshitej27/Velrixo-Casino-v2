# admin.py
from aiogram import types
from aiogram.filters import Command
from database import is_admin, add_admin, remove_admin, make_code, change_balance, get_balance, _cur
from utils import fmt_amount

async def makecode_cmd(message: types.Message):
    uid = message.from_user.id
    if not is_admin(uid):
        await message.reply("❌ Only admins can use this.")
        return
    parts = message.get_args().split()
    if len(parts) < 2:
        await message.reply("Usage: /makecode CODE AMOUNT [uses_allowed]")
        return
    code = parts[0].upper()
    try:
        amount = int(parts[1])
    except:
        await message.reply("Enter numeric amount.")
        return
    uses_allowed = int(parts[2]) if len(parts) >= 3 else 1
    make_code(code, amount, uses_allowed, uid)
    await message.reply(f"✅ Code {code} created: {fmt_amount(amount)} x{uses_allowed}")

async def addadmin_cmd(message: types.Message):
    uid = message.from_user.id
    if not is_admin(uid):
        await message.reply("Only admins.")
        return
    try:
        new_id = int(message.get_args().strip())
    except:
        await message.reply("Provide numeric user id.")
        return
    add_admin(new_id)
    await message.reply(f"✅ Added admin: {new_id}")

async def removeadmin_cmd(message: types.Message):
    uid = message.from_user.id
    if not is_admin(uid):
        await message.reply("Only admins.")
        return
    try:
        rem_id = int(message.get_args().strip())
    except:
        await message.reply("Provide numeric user id.")
        return
    remove_admin(rem_id)
    await message.reply(f"✅ Removed admin: {rem_id}")

async def givepacket_cmd(message: types.Message):
    uid = message.from_user.id
    if not is_admin(uid):
        await message.reply("Only admins.")
        return
    parts = message.get_args().split()
    if len(parts) < 2:
        await message.reply("Usage: /givepacket <user_id_or_@username> <amount>")
        return
    target = parts[0]
    try:
        amt = int(parts[1])
    except:
        await message.reply("Amount numeric.")
        return
    # try username or id
    if target.startswith("@"):
        name = target.lstrip("@")
        _cur.execute("SELECT user_id FROM users WHERE username=? COLLATE NOCASE", (name,))
        r = _cur.fetchone()
        if not r:
            await message.reply("User not registered (they must /start first).")
            return
        user_id = r[0]
    else:
        try:
            user_id = int(target)
        except:
            await message.reply("Invalid target.")
            return
    from database import give_packet
    give_packet(user_id, amt)
    await message.reply(f"✅ Assigned packet {fmt_amount(amt)} to {target}")

async def broadcast_cmd(message: types.Message):
    uid = message.from_user.id
    if not is_admin(uid):
        await message.reply("Only admins.")
        return
    text = message.get_args().strip()
    if not text:
        await message.reply("Usage: /broadcast <message>")
        return
    _cur.execute("SELECT user_id FROM users")
    users = _cur.fetchall()
    sent = 0
    for (u,) in users:
        try:
            await message.bot.send_message(u, f"📢 Admin broadcast:\n\n{text}")
            sent += 1
        except:
            pass
    await message.reply(f"Broadcast attempted to {sent} users.")
