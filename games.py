# games.py
import random
from aiogram import types
from aiogram.filters import Command
from database import get_balance, change_balance, ensure_user, get_user_row
from utils import fmt_amount

# maximum bet rule: 10% of balance (prevents runaway inflation)
def max_bet_allowed(uid:int, requested:int) -> int:
    bal = get_balance(uid)
    if bal <= 0:
        return 0
    limit = max(1, bal // 10)
    return min(requested, limit)

# ---- animated slot (uses Telegram 🎰 dice animation) ----
async def slot_cmd(message: types.Message):
    uid = message.from_user.id
    args = message.get_args().strip()
    # optional bet param: if provided use it (but slots default 100)
    bet = 100
    if args:
        try:
            bet = int(args)
        except:
            pass
    bet = max(1, bet)
    if bet > get_balance(uid):
        await message.reply("❌ Not enough balance.")
        return
    # restrict to 10% of balance
    bet = max_bet_allowed(uid, bet)
    # send animated slot
    dice_msg = await message.answer_dice(emoji="🎰")
    # Telegram slot value range varies; treat > 40 as big win heuristic
    val = getattr(dice_msg.dice, "value", None)
    # fallback to random if none
    if val is None:
        val = random.randint(1,64)
    # compute simple payout:
    if val >= 60:
        win = bet * 6
        change_balance(uid, win)
        await message.reply(f"🎰 {dice_msg.dice.value} — JACKPOT! +{fmt_amount(win)}")
    elif val >= 40:
        win = bet * 2
        change_balance(uid, win)
        await message.reply(f"🎰 {dice_msg.dice.value} — Nice! +{fmt_amount(win)}")
    else:
        change_balance(uid, -bet)
        await message.reply(f"🎰 {dice_msg.dice.value} — You lost {fmt_amount(bet)}")

# ---- animated dice (🎲) simple guess or roll ----
async def dice_cmd(message: types.Message):
    uid = message.from_user.id
    args = message.get_args().strip().split()
    # optional: /dice <amount> to bet on '6' (win big) else fixed fun roll
    if not args:
        # just roll for fun (no bet)
        dice_msg = await message.answer_dice(emoji="🎲")
        v = getattr(dice_msg.dice, "value", 0)
        await message.reply(f"🎲 You rolled *{v}*", parse_mode="Markdown")
        return
    try:
        bet = int(args[0])
    except:
        await message.reply("Enter numeric bet.")
        return
    bet = max_bet_allowed(uid, bet)
    if bet == 0 or bet > get_balance(uid):
        await message.reply("Not enough balance.")
        return
    dice_msg = await message.answer_dice(emoji="🎲")
    v = getattr(dice_msg.dice, "value", random.randint(1,6))
    if v == 6:
        win = bet * 3
        change_balance(uid, win)
        await message.reply(f"🎲 Rolled {v} — You win {fmt_amount(win)}")
    else:
        change_balance(uid, -bet)
        await message.reply(f"🎲 Rolled {v} — You lost {fmt_amount(bet)}")

# ---- dart (animated 🎯) ----
async def dart_cmd(message: types.Message):
    uid = message.from_user.id
    args = message.get_args().strip().split()
    if not args:
        await message.reply("Usage: /dart <amount>")
        return
    try:
        bet = int(args[0])
    except:
        await message.reply("Enter numeric amount.")
        return
    bet = max_bet_allowed(uid, bet)
    if bet == 0 or bet > get_balance(uid):
        await message.reply("Not enough balance.")
        return
    dice_msg = await message.answer_dice(emoji="🎯")
    v = getattr(dice_msg.dice, "value", random.randint(1,6))
    # dart returns 1-6; treat 6 as bullseye
    if v == 6:
        win = bet * 2
        change_balance(uid, win)
        await message.reply(f"🎯 Bullseye! You won {fmt_amount(win)}")
    elif v >= 4:
        win = bet
        change_balance(uid, win)
        await message.reply(f"🎯 Good! You won {fmt_amount(win)}")
    else:
        change_balance(uid, -bet)
        await message.reply(f"🎯 Missed. You lost {fmt_amount(bet)}")

# ---- bowling (animated 🎳) ----
async def bowl_cmd(message: types.Message):
    uid = message.from_user.id
    args = message.get_args().strip().split()
    if not args:
        await message.reply("Usage: /bowl <amount>")
        return
    try:
        bet = int(args[0])
    except:
        await message.reply("Enter numeric amount.")
        return
    bet = max_bet_allowed(uid, bet)
    if bet == 0 or bet > get_balance(uid):
        await message.reply("Not enough.")
        return
    dice_msg = await message.answer_dice(emoji="🎳")
    v = getattr(dice_msg.dice, "value", random.randint(1,6))
    # 6 = strike
    if v == 6:
        win = int(bet * 3)
        change_balance(uid, win)
        await message.reply(f"🎳 Strike! You won {fmt_amount(win)}")
    elif v >= 4:
        win = int(bet * 1.5)
        change_balance(uid, win)
        await message.reply(f"🎳 Good throw! You won {fmt_amount(win)}")
    else:
        change_balance(uid, -bet)
        await message.reply(f"🎳 Gutter. You lost {fmt_amount(bet)}")

# ---- football (animated ⚽) ----
async def football_cmd(message: types.Message):
    uid = message.from_user.id
    args = message.get_args().strip().split()
    if not args:
        await message.reply("Usage: /football <amount>")
        return
    try:
        bet = int(args[0])
    except:
        await message.reply("Enter numeric amount.")
        return
    bet = max_bet_allowed(uid, bet)
    if bet == 0 or bet > get_balance(uid):
        await message.reply("Not enough.")
        return
    dice_msg = await message.answer_dice(emoji="⚽")
    v = getattr(dice_msg.dice, "value", random.randint(1,6))
    # treat 5-6 as GOAL
    if v >= 5:
        win = bet * 2
        change_balance(uid, win)
        await message.reply(f"⚽ Goal! You won {fmt_amount(win)}")
    else:
        change_balance(uid, -bet)
        await message.reply(f"⚽ Miss. You lost {fmt_amount(bet)}")
