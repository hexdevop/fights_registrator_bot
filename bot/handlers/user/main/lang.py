from aiogram import types, Router, F
from aiogram.filters import Command

from bot import Cache
from bot.filters.buttons import Button
from bot.filters.dont_selected_language import DontSelectedLangFilter
from bot.keyboards.user import inline, reply
from config import config

router = Router(name='lang')


@router.message(DontSelectedLangFilter())
async def send_message_with_language_buttons(
        message: types.Message,
):
    await message.answer(
        text='Выберите язык / Tilni tanlang:',
        reply_markup=inline.languages()
    )

@router.message(Button('select-language'))
@router.message(Command('lang'))
async def send_message_with_language_buttons(
        message: types.Message,
):
    await message.answer(
        text='Выберите язык / Tilni tanlang:',
        reply_markup=inline.languages()
    )


@router.callback_query(F.data.startswith('select_lang'))
async def select_language(
        call: types.CallbackQuery,
        cache: Cache,
):
    lang = call.data.split(':')[1]
    await cache.set_user_language(call.from_user.id, lang)
    l10n = cache.get_l10n(lang)
    await call.message.delete()
    await call.message.answer(
        text=l10n.format_value('start', {'first_name': call.from_user.first_name}),
        reply_markup=reply.main_menu(l10n, call.from_user.id in config.bot.admins),
    )
