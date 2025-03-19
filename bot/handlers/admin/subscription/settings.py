from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from fluent.runtime.types import fluent_number
from sqlalchemy import select, update, case, delete

from bot.handlers.admin.subscription.main import subscription_list
from database import get_master_session, get_slave_session
from database.models import Subscription
from bot.keyboards.admin import inline
from bot.keyboards.admin.factory import SubscriptionCallbackData
from bot.states import SubscriptionState
from bot.utils import helper
from bot.enums import Status

router = Router()


@router.callback_query(SubscriptionCallbackData.filter(F.action == "settings"))
async def subscription_settings(
    event: types.CallbackQuery | types.Message,
    callback_data: SubscriptionCallbackData,
    l10n: FluentLocalization,
    edit: bool = True,
):
    async with get_slave_session() as session:
        subscription: Subscription = await session.scalar(
            select(Subscription).where(Subscription.id == callback_data.id)
        )
    message = event if isinstance(event, types.Message) else event.message
    method = message.edit_text if edit else message.answer
    await method(
        text=l10n.format_value(
            'subscription-settings-channel',
            {
                "id": subscription.id,
                "status": subscription.status.value,
                "title": subscription.title,
                "chat_id": fluent_number(subscription.chat_id, useGrouping=False),
                "username": subscription.username or l10n.format_value("null"),
                "url": subscription.url,
                "users": len(subscription.users),
            },
        ),
        reply_markup=inline.subscription_settings(callback_data)
    )



@router.callback_query(SubscriptionCallbackData.filter(F.action == "change-status"))
async def change_working_status(
    call: types.CallbackQuery,
    callback_data: SubscriptionCallbackData,
    l10n: FluentLocalization,
):
    async with get_master_session() as session:
        async with session.begin():
            await session.execute(
                update(Subscription)
                .where(Subscription.id == callback_data.id)
                .values(
                    status=case(
                        (Subscription.status == Status.STOPPED, Status.AVAILABLE.name),
                        (Subscription.status == Status.AVAILABLE, Status.STOPPED.name),
                        else_=Subscription.status,
                    )
                )
            )
    await subscription_settings(call, callback_data, l10n)


@router.callback_query(SubscriptionCallbackData.filter(F.action == "change-url"))
async def start_change_url(
    call: types.CallbackQuery,
    callback_data: SubscriptionCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    message_id = (
        await call.message.edit_text(
            text=l10n.format_value("send-new-url-for-subscription"),
            reply_markup=inline.cancel(callback_data, "settings"),
        )
    ).message_id
    await state.update_data(callback_data=callback_data.model_dump())
    await state.update_data(message_id=message_id)
    await state.set_state(SubscriptionState.url)


@router.message(SubscriptionState.url, F.text)
async def get_new_url(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = SubscriptionCallbackData.model_validate(data.get("callback_data"))

    if len(message.text.split()) < 2 and "t.me" in message.text:
        async with get_master_session() as session:
            async with session.begin():
                await session.execute(
                    update(Subscription)
                    .where(Subscription.id == callback_data.id)
                    .values(url=message.text.strip())
                )
        await subscription_settings(message, callback_data, l10n, edit=False)
    else:
        message_id = (
            await message.answer(
                text=l10n.format_value("its-not-telegram-url"),
                reply_markup=inline.cancel(callback_data, "settings"),
            )
        ).message_id
        await state.update_data(message_id=message_id)


@router.callback_query(SubscriptionCallbackData.filter(F.action == "delete"))
async def delete_subscription(
    call: types.CallbackQuery,
    callback_data: SubscriptionCallbackData,
    l10n: FluentLocalization,
):
    await call.message.edit_text(
        text=l10n.format_value("confirm-deleting"),
        reply_markup=inline.confirm(callback_data, cancel_value="settings"),
    )


@router.callback_query(SubscriptionCallbackData.filter(F.action == "confirm"))
async def confirm_deleting(
    call: types.CallbackQuery,
    callback_data: SubscriptionCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    async with get_master_session() as session:
        async with session.begin():
            chat_id = await session.scalar(
                select(Subscription.chat_id).where(
                    Subscription.id == callback_data.id,
                )
            )
            if chat_id is not None:
                await call.bot.leave_chat(chat_id=chat_id)
            await session.execute(
                delete(Subscription).where(Subscription.id == callback_data.id)
            )
    await call.message.edit_text(text=l10n.format_value("successfully-deleted"))
    await subscription_list(call, state, l10n, edit=False, page=callback_data.page)

