from aiogram import Dispatcher
from loguru import logger

from . import (
    lang,
    start,
)

def reg_routers(dp: Dispatcher):
    handlers = [
        lang,
        start,
    ]
    for handler in handlers:
        dp.include_router(handler.router)
    logger.opt(colors=True).info(
        f"<fg #abffaa>[user.main {len(handlers)} files imported]</>"
    )
