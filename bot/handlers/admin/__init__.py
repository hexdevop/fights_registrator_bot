from aiogram import Dispatcher
from loguru import logger

from . import (
    mover,
    commands,
    subscription,
    tournament,
    regions,
)
from bot.filters.admin import AdminFilter


def reg_routers(dp: Dispatcher):
    handlers = [
        mover,
        commands,
        regions,
    ]
    for handler in handlers:
        handler.router.message.filter(AdminFilter())
        dp.include_router(handler.router)
    logger.opt(colors=True).info(
        f"<fg #ffb4aa>[admin {len(handlers)} handlers imported]</>"
    )
    subscription.reg_routers(dp)
    tournament.reg_routers(dp)
