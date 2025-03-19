import asyncio
import sys
from loguru import logger

from bot import handlers, middlewares, dp, bot
from bot.utils.ui_commands import set_bot_commands
from config import config

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> <red>|</red> "
    "<level>{level: <8}</level> <red>|</red> "
    "<level>{message}</level>"
)
logger.remove()  # Удаляем предыдущие конфигурации
logger.add(sys.stdout, format=logger_format)

logger.info(f"Attempting Bot Startup")

handlers.setup(dp)
middlewares.setup(dp)

updates = dp.resolve_used_update_types()
logger.opt(colors=True).info(
    "Allowed updates: <fg #00ccff>[%s]</>" % ", ".join(updates)
)


async def main():

    await set_bot_commands(bot)

    config.bot.username = (await bot.get_me()).username

    logger.info(f"All utils of @{config.bot.username} STARTED WITH POLLING")

    if config.bot.skip_updates:
        await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=updates)

if __name__ == "__main__":
    asyncio.run(main())
