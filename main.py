# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import BOT_TOKEN
import database

# import handlers
import games
import admin
import economy_handlers as econ

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("velrixo_v2")

async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set. Set environment variable BOT_TOKEN before running.")
        return

    # initialize DB
    database.init_db()

    # create bot & dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register economy handlers
    dp.message.register(econ.start_handler, Command(commands=["start"]))
    dp.message.register(econ.profile_handler, Command(commands=["profile"]))
    dp.message.register(econ.daily_handler, Command(commands=["daily"]))
    dp.message.register(econ.redeem_handler, Command(commands=["redeem"]))
    dp.message.register(econ.referral_handler, Command(commands=["referral"]))
    dp.message.register(econ.leaderboard_handler, Command(commands=["leaderboard"]))
    dp.message.register(econ.start_handler, Command(commands=["help"]))  # reuse start/help

    # Register game handlers (animated)
    dp.message.register(games.slot_cmd, Command(commands=["slot","slots"]))
    dp.message.register(games.dice_cmd, Command(commands=["dice"]))
    dp.message.register(games.dart_cmd, Command(commands=["dart"]))
    dp.message.register(games.bowl_cmd, Command(commands=["bowl","bowling"]))
    dp.message.register(games.football_cmd, Command(commands=["football"]))
    # you can add /crash custom (non-animated) later if desired

    # Admin handlers
    dp.message.register(admin.makecode_cmd, Command(commands=["makecode"]))
    dp.message.register(admin.addadmin_cmd, Command(commands=["addadmin"]))
    dp.message.register(admin.removeadmin_cmd, Command(commands=["removeadmin"]))
    dp.message.register(admin.givepacket_cmd, Command(commands=["givepacket"]))
    dp.message.register(admin.broadcast_cmd, Command(commands=["broadcast"]))

    logger.info("Velrixo Casino Bot V2 starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
