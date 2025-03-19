from aiogram.filters import BaseFilter


class DontSelectedLangFilter(BaseFilter):
    async def __call__(self, event, lang: str | None) -> bool:
        return lang is None
