from aiogram.utils.keyboard import ReplyKeyboardBuilder
from fluent.runtime import FluentLocalization


def main_menu(l10n: FluentLocalization, is_admin: bool = False):
    builder = ReplyKeyboardBuilder()
    builder.button(text=l10n.format_value("register"))
    builder.button(text=l10n.format_value("select-language"))
    sizes = [1, 1]
    sub_size = 0
    if is_admin:
        builder.button(text="Панель администратора ⚙️")
        sub_size += 1
    if sub_size:
        sizes.append(sub_size)
    return builder.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder="Главное меню 💠"
    )
