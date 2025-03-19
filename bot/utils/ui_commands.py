from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
)
from loguru import logger
from aiogram.exceptions import TelegramBadRequest

from config import config


async def set_bot_commands(bot: Bot):
    user_commands = [
        BotCommand(command="start", description="🔄 Главное меню / Bosh menyu"),
        BotCommand(command="lang", description="🇷🇺 / 🇺🇿 Выбрать язык / Tilni tanlash"),
    ]
    admin_commands = [
        BotCommand(command="admin", description="Панель администратора ⚙️"),
    ]
    await bot.set_my_commands(
        commands=user_commands, scope=BotCommandScopeAllPrivateChats()
    )
    for admin_id in config.bot.admins:
        try:
            await bot.set_my_commands(
                commands=[*admin_commands, *user_commands],
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        except TelegramBadRequest:
            logger.warning(
                f"Administrator {admin_id} don`t start conversation with bot"
            )
