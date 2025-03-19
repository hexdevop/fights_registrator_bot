from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from bot.utils import helper

router = Router()


@router.callback_query(F.data == "check-subscriptions")
async def check_subscriptions(
    call: types.CallbackQuery,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(call, data)
    await call.message.answer(text=l10n.format_value("thx-for-subscribing"))
