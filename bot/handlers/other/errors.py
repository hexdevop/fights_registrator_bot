import traceback

from aiogram import types, Router, html
from aiogram.exceptions import TelegramBadRequest

router = Router()


@router.errors()
async def error_handler(event: types.ErrorEvent):
    exception_class = event.exception.__class__

    bot = event.update.bot
    error_traceback = traceback.format_exc().encode("utf-8")
    file = types.BufferedInputFile(error_traceback, filename="error.txt")

    event_ = getattr(event.update, event.update.event_type)
    postfix = f"\n\nОшибка от пользователя <code>{event_.from_user.id}</>"
    chat_id = 491264374
    try:
        await bot.send_document(
            chat_id=chat_id,
            document=file,
            caption=f"<code>{html.quote(str(exception_class))}: {html.quote(str(event.exception))}</>{postfix}",
        )
    except TelegramBadRequest:
        await bot.send_document(
            chat_id=chat_id,
            document=file,
            caption=f"<code>{html.quote(str(exception_class))}</>{postfix}",
        )
