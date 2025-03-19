from aiogram import types, Router, F

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from config import config
from bot.keyboards.user import reply

router = Router(name="start")


@router.message(Command("start", magic=F.text.split().len() == 1))
async def start_command(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await state.clear()
    await message.answer(
        text=l10n.format_value('start', {'first_name': message.from_user.first_name}),
        reply_markup=reply.main_menu(l10n, message.from_user.id in config.bot.admins),
    )


