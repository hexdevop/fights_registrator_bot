from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from sqlalchemy import select
from sqlalchemy.orm import defer

from config import config
from database import get_slave_session
from database.models import Subscription
from bot.keyboards.admin import inline
from bot.keyboards.admin.factory import SubscriptionCallbackData

router = Router()


@router.message(F.text == "ОП 🔐")
async def subscription_list(
    event: types.Message | types.CallbackQuery,
    state: FSMContext,
    l10n: FluentLocalization,
    edit: bool = False,
    page: int = 1,
):
    await state.clear()
    message = event if isinstance(event, types.Message) else event.message
    method = message.edit_text if edit else message.answer
    async with get_slave_session() as session:
        subscriptions = (
            await session.scalars(
                select(Subscription).options(defer(Subscription.users))
            )
        ).all()
    await method(
        text=l10n.format_value("subscription", {"username": config.bot.username}),
        reply_markup=inline.subscriptions_list(subscriptions, page=page),
    )


@router.callback_query(SubscriptionCallbackData.filter(F.action == "main"))
async def return_to_main_list(
    call: types.CallbackQuery,
    callback_data: SubscriptionCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await subscription_list(call, state, l10n, edit=True, page=callback_data.page)


@router.callback_query(SubscriptionCallbackData.filter(F.action == "page"))
async def pagination(
    call: types.CallbackQuery,
    callback_data: SubscriptionCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await subscription_list(call, state, l10n, edit=True, page=callback_data.page)
    await call.answer(text=l10n.format_value("page", {"page": callback_data.page}))


@router.callback_query(SubscriptionCallbackData.filter(F.action == "length"))
async def length_of_list(
    call: types.CallbackQuery,
    l10n: FluentLocalization,
):
    await call.answer(text=l10n.format_value("length-of-list"), show_alert=True)
