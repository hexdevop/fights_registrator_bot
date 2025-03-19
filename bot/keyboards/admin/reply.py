from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_admin():
    builder = ReplyKeyboardBuilder()
    builder.button(text="ОП 🔐")
    builder.button(text="Турниры 💪")
    builder.button(text="Регионы 🏳️")
    builder.button(text="🔙 Панель подписчиков")
    return builder.adjust(1, 2, 1).as_markup(
        resize_keyboard=True, input_field_placeholder="Админ панель 🏚"
    )
