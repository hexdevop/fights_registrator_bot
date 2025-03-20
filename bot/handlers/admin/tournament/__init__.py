from aiogram import Dispatcher
from loguru import logger

from . import (
    main,
    create,
    settings,
    discipline,
    download,
)
from bot.filters.admin import AdminFilter


def reg_routers(dp: Dispatcher):
    handlers = [
        main,
        create,
        settings,
        discipline,
        download,
    ]
    for handler in handlers:
        handler.router.message.filter(AdminFilter())
        dp.include_router(handler.router)
    logger.opt(colors=True).info(
        f"<fg #ffb4aa>[admin.tournament {len(handlers)} handlers imported]</>"
    )
