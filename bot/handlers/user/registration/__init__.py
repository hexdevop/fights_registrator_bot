from aiogram import Dispatcher
from loguru import logger

from bot.middlewares import SubscriptionMiddleware

from . import (
    registration,
    subscription,
)

def reg_routers(dp: Dispatcher):
    handlers = [
        registration,
        subscription,
    ]
    for handler in handlers:
        handler.router.message.middleware(SubscriptionMiddleware())
        handler.router.callback_query.middleware(SubscriptionMiddleware())

        dp.include_router(handler.router)
    logger.opt(colors=True).info(
        f"<fg #abffaa>[user.registration {len(handlers)} files imported]</>"
    )
