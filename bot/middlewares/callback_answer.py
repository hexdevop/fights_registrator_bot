from typing import Callable, Dict, Any, Awaitable

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.utils.callback_answer import CallbackAnswerMiddleware


class CallbackAnswer(CallbackAnswerMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        try:
            await super().__call__(handler, event, data)
        except TelegramBadRequest:
            pass
        finally:
            await event.answer()
