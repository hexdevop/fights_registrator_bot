from aiogram import types, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from sqlalchemy import text
from tabulate import tabulate

from database import get_master_session

router = Router()


@router.message(Command("file_id"))
async def get_file_id(message: types.Message, command: CommandObject):
    if message.reply_to_message and message.reply_to_message.content_type != "text":
        if message.reply_to_message.content_type == "photo":
            return await message.answer(text=message.reply_to_message.photo[-1].file_id)
        await message.answer(
            text=getattr(
                message.reply_to_message, message.reply_to_message.content_type
            ).file_id
        )
    if command.args:
        try:
            try:
                await message.answer_photo(photo=command.args)
            except TelegramBadRequest:
                await message.answer_animation(animation=command.args)
        except Exception as err:
            await message.answer(text=str(err))


@router.message(Command("sql"))
async def sql_command(
    message: types.Message,
    command: CommandObject,
):
    if not command.args:
        await message.reply(
            "Пожалуйста, укажите SQL-запрос. Пример: /sql SELECT * FROM users;"
        )
        return

    query = command.args

    try:
        async with get_master_session() as session:
            async with session.begin():
                result = await session.execute(text(query))

                affected_rows = result.rowcount

                if query.strip().lower().startswith(
                    "select"
                ) or query.strip().lower().startswith("show"):
                    rows = result.fetchall()
                    if rows:
                        headers = result.keys()
                        response = tabulate(rows, headers=headers, tablefmt="pretty")
                    else:
                        response = "Результатов нет."
                else:
                    await session.commit()
                    response = "Запрос выполнен успешно."

        response += f"\n\nЗатронуто записей: {affected_rows}"

        await message.reply(f"```\n{response}\n```", parse_mode="Markdown")

    except Exception as e:
        # Обработка ошибок
        await message.reply(f"Ошибка при выполнении запроса: {e}")
