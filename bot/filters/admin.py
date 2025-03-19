from aiogram.filters import BaseFilter

from bot import Cache
from config import config


class AdminFilter(BaseFilter):
    async def __call__(self, event, cache: Cache) -> bool:
        if event.from_user.id in config.bot.admins:
            return {"l10n": cache.get_l10n("ru")}