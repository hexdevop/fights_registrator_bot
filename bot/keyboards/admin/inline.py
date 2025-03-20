from math import ceil

from database.models import Subscription
from bot.keyboards.admin.factory import SubscriptionCallbackData, TournamentCallbackData, RegionCallbackData
from bot.keyboards.utils import *
from bot.enums import Status
from database.models.admin import Tournament, Discipline, Region


def skip_or_cancel(data: SubscriptionCallbackData, cancel_value: str = None):
    builder = InlineKeyboardBuilder()
    data.action = "skip"
    builder.button(text="Пропустить ⏩", callback_data=data.pack())
    data.action = cancel_value or "main"
    builder.button(text="🚫 Отмена", callback_data=data.pack())
    return builder.adjust(1).as_markup()


def subscriptions_list(
    subscriptions: List[Subscription],
    width: int = 1,
    height: int = 8,
    page: int = 1,
):
    builder = InlineKeyboardBuilder()
    s = width * height
    length = ceil(len(subscriptions) / s)
    data = SubscriptionCallbackData(
        action="settings",
        page=page,
    )
    for subscription in subscriptions[s * (page - 1) : s * page]:
        data.id = subscription.id
        name = (
            (subscription.title[:25] + "...")
            if len(subscription.title) > 25
            else subscription.title
        )
        builder.button(
            text=f'{name} | {"🟢" if subscription.status == Status.AVAILABLE else "🔴"}',
            callback_data=data.pack(),
        )
    sizes = []
    sizes = generate_sizes(sizes, subscriptions, width, height, page)
    builder, sizes = with_pagination(
        builder, data, length, page, sizes, as_markup=False
    )
    data.action = "add-channel"
    builder.button(text="➕", callback_data=data.pack())
    sizes.append(1)
    return builder.adjust(*sizes).as_markup()

def subscription_settings(
    data: SubscriptionCallbackData,
):
    builder = InlineKeyboardBuilder()
    data.action = "change-status"
    builder.button(text="🛠 Сменить статус", callback_data=data.pack())
    data.action = "change-url"
    builder.button(text="✍️ Сменить ссылку 🌐", callback_data=data.pack())
    data.action = "delete"
    builder.button(text="🗑 Удалить", callback_data=data.pack())
    data.action = "main"
    builder.button(text="🔙 Назад", callback_data=data.pack())
    return builder.adjust(1).as_markup()


def tournament_list(tournaments: list[Tournament], tournaments_count: int, page: int):
    builder = InlineKeyboardBuilder()
    data = TournamentCallbackData(action='settings')
    length = ceil(tournaments_count / 10)
    for i in tournaments:
        data.id = i.id
        builder.button(
            text=i.name,
            callback_data=data.pack()
        )
    sizes = generate_sizes([], tournaments, 1, 10, 1)
    data.action = 'add'
    builder.button(
        text='➕ Добавить турнир',
        callback_data=data.pack()
    )
    sizes.append(1)
    return with_pagination(builder, data, length, page, sizes)


def tournament_settings(data: TournamentCallbackData, status: Status):
    builder = InlineKeyboardBuilder()
    data.action = 'disciplines'
    builder.button(
        text='📔 Дисциплины',
        callback_data=data.pack()
    )
    data.action = 'status'
    builder.button(
        text='🔴 Остановить регистрацию' if status == Status.AVAILABLE else '🟢 Включить регистрацию',
        callback_data=data.pack()
    )
    data.action = 'download'
    builder.button(text='🌐 Скачать данные турнира', callback_data=data.pack())
    data.action = "delete"
    builder.button(text="🗑 Удалить", callback_data=data.pack())
    data.action = "main"
    builder.button(text="🔙 Назад", callback_data=data.pack())
    return builder.adjust(1).as_markup()


def disciplines_list(data: TournamentCallbackData,disciplines: list[Discipline]):
    builder = InlineKeyboardBuilder()
    for i in disciplines:
        data.action = 'ok'
        data.discipline_id = i.id
        builder.button(
            text=i.name,
            callback_data=data.pack()
        )
        data.action = 'delete-discipline'
        builder.button(
            text='Удалить 🗑',
            callback_data=data.pack()
        )
    sizes = [2] * len(disciplines)
    data.action = 'add-discipline'
    builder.button(
        text='➕ Добавить дисциплину',
        callback_data=data.pack()
    )
    sizes.append(1)
    data.action = 'settings'
    builder.button(
        text=back_text,
        callback_data=data.pack()
    )
    return builder.adjust(*sizes).as_markup()


def regions_list(regions: list[Region], regions_count: int, page: int):
    builder = InlineKeyboardBuilder()
    data = RegionCallbackData(action='ok')

    length = ceil(regions_count / 10)
    for i in regions:
        data.action = 'ok'
        data.id = i.id
        builder.button(
            text=i.name,
            callback_data=data.pack()
        )
        data.action = 'delete'
        builder.button(
            text='Удалить 🗑',
            callback_data=data.pack()
        )
    sizes = [2] * len(regions)
    data.action = 'add'
    builder.button(
        text='➕ Добавить регион',
        callback_data=data.pack()
    )
    sizes.append(1)
    return with_pagination(builder, data, length, page, sizes)
