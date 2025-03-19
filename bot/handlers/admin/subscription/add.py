from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from bot.handlers.admin.subscription.main import subscription_list
from database import get_master_session
from database.models import Subscription
from bot.keyboards.admin import inline, reply
from bot.keyboards.admin.factory import SubscriptionCallbackData
from bot.states import SubscriptionState
from bot.utils import helper

router = Router()

@router.callback_query(SubscriptionCallbackData.filter(F.action == "add-channel"))
async def add_channel_button(
    call: types.CallbackQuery,
    callback_data: SubscriptionCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    message_id = (
        await call.message.edit_text(
            text=l10n.format_value("forward-message-from-channel"),
            reply_markup=inline.cancel(callback_data, "main"),
        )
    ).message_id
    await state.update_data(message_id=message_id)
    await state.update_data(callback_data=callback_data.model_dump())
    await state.set_state(SubscriptionState.message_from_channel)


@router.message(SubscriptionState.message_from_channel)
async def get_message_from_channel(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = SubscriptionCallbackData.model_validate(data.get("callback_data"))
    if message.forward_from_chat:
        message_id = (
            await message.answer(
                text=l10n.format_value("get-channel-link"),
                reply_markup=inline.cancel(callback_data, "main"),
            )
        ).message_id
        await state.update_data(message_id=message_id)
        await state.update_data(chat_id=message.forward_from_chat.id)
        await state.update_data(title=message.forward_from_chat.title)
        await state.update_data(username=message.forward_from_chat.username)
        await state.set_state(SubscriptionState.channel_link)
    else:
        message_id = (
            await message.answer(
                text=l10n.format_value("forward-message-from-channel"),
                reply_markup=inline.cancel(callback_data, "main"),
            )
        ).message_id
        await state.update_data(message_id=message_id)


@router.message(SubscriptionState.channel_link)
async def get_channel_link(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = SubscriptionCallbackData.model_validate(data.get("callback_data"))
    if "t.me" in message.text:
        subscription = Subscription(
            chat_id=data.get("chat_id"),
            title=data.get("title"),
            username=data.get("username"),
            url=message.text,
        )
        async with get_master_session() as session:
            async with session.begin():
                session.add(subscription)
        await message.answer(
            text=l10n.format_value(
                "channel-success-add", {"title": subscription.title}
            ),
            reply_markup=reply.main_admin(),
        )
        await subscription_list(message, state, l10n, page=callback_data.page)
    else:
        message_id = (
            await message.answer(
                text=l10n.format_value("get-channel-link"),
                reply_markup=inline.cancel(callback_data, "main"),
            )
        ).message_id
        await state.update_data(message_id=message_id)