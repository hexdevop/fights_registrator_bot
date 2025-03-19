from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from bot.keyboards.admin import reply

from bot.keyboards.user.reply import main_menu

router = Router()


@router.message(Command("admin"))
@router.message(F.text == "Панель администратора ⚙️")
@router.message(F.text == "🔙 Назад в админ панель 🏚")
async def move_to_admin_menu(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await state.clear()
    await message.answer(
        text=l10n.format_value("admin-menu"), reply_markup=reply.main_admin()
    )


@router.message(F.text == "🔙 Панель подписчиков")
async def move_to_admin_menu(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await state.clear()
    await message.answer(
        text=l10n.format_value("start", {'first_name': message.from_user.first_name}), reply_markup=main_menu(l10n, True)
    )
