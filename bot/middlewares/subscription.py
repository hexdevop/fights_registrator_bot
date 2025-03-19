from typing import Any, Awaitable, Dict, Callable, Union

from aiogram import BaseMiddleware, types, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from fluent.runtime import FluentLocalization
from sqlalchemy import select
from sqlalchemy.orm import defer

from config import config
from database import get_master_session
from bot.keyboards.user import inline
from bot.utils import helper
from database.models import Subscription

from bot.enums import Status


class SubscriptionMiddleware(BaseMiddleware):
    _instance = None

    def __init__(self):
        super().__init__()
        self.bot: Bot = None
        self.flyer = None
        self.bots = {}
        self.message_id = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def __call__(
        self,
        handler: Callable[
            [types.Message | types.CallbackQuery, Dict[str, Any]], Awaitable[Any]
        ],
        event: Union[types.Message | types.CallbackQuery, Any],
        data: Dict[str, Any],
    ) -> Any:
        user: types.User = data.get("event_from_user")
        async with get_master_session() as session:
            async with session.begin():
                data["session"] = session
                if self.bot is None:
                    self.bot = event.bot
                l10n: FluentLocalization = data.get("l10n")
                if user.id not in config.bot.admins:
                    subscriptions = (
                        await session.scalars(
                            select(Subscription)
                            .options(defer(Subscription.users))
                            .where(
                                ~Subscription.users.contains(user.id),
                                Subscription.status == Status.AVAILABLE,
                            )
                        )
                    ).all()
                    to_button = []
                    for subscription in subscriptions:
                        if not await self.subbed(subscription, user):
                            to_button.append(subscription)
                    if to_button:
                        text = "subscribe-for-using-bot"
                        message_id = self.message_id.get(user.id, None)
                        if message_id is not None:
                            await helper.delete_message(self.bot, user.id, message_id)
                            text = "subscribe-to-all-resources"
                        self.message_id[user.id] = (
                            await self.bot.send_message(
                                chat_id=user.id,
                                text=l10n.format_value(text),
                                reply_markup=inline.subscription(l10n, to_button),
                            )
                        ).message_id
                        return

                    message_id = self.message_id.get(user.id, None)
                    if message_id is not None:
                        await helper.delete_message(self.bot, user.id, message_id)
                        self.message_id.pop(user.id)

                await handler(event, data)

    async def subbed(self, subscription: Subscription, user: types.User):
        try:
            member = await self.bot.get_chat_member(
                chat_id=subscription.chat_id, user_id=user.id
            )
            if member.status == ChatMemberStatus.LEFT:
                return False
        except TelegramBadRequest:
            return False
