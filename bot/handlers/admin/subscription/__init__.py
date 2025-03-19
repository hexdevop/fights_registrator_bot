from aiogram import Dispatcher
from loguru import logger

from . import (
    main,
    add,
    settings,
)
from bot.filters.admin import AdminFilter


def reg_routers(dp: Dispatcher):
    handlers = [
        main,
        add,
        settings,
    ]
    for handler in handlers:
        handler.router.message.filter(AdminFilter())
        dp.include_router(handler.router)
    logger.opt(colors=True).info(
        f"<fg #ffb4aa>[admin.subscription {len(handlers)} handlers imported]</>"
    )
