from aiogram import Dispatcher
from loguru import logger

from . import errors


def reg_routers(dp: Dispatcher):
    handlers = [errors]
    for handler in handlers:
        dp.include_router(handler.router)
    logger.opt(colors=True).info(
        f"<fg #ffaaf1>[other {len(handlers)} handlers imported]</>"
    )
