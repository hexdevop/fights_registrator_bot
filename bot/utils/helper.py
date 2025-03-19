import re

from aiogram import types, exceptions, Bot


def has_cyrillic(text):
    return bool(re.search("[а-яА-Я]", text))


async def delete_messages(
    event: types.Message | types.CallbackQuery, data: dict = None, user_id: int = None
):
    try:
        if isinstance(event, types.Message):
            message_ids = [event.message_id]
        else:
            message_ids = [event.message.message_id]
        if data:
            message_ids += data.get("message_ids", [])
            if "message_id" in data.keys():
                message_ids.append(data.get("message_id"))
        await event.bot.delete_messages(
            chat_id=user_id or event.from_user.id, message_ids=message_ids
        )
    except exceptions.TelegramBadRequest:
        pass


async def delete_message(bot: Bot, user_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=user_id, message_id=message_id)
    except exceptions.TelegramBadRequest:
        pass
