from bot.keyboards.user.factory import RegCallback
from bot.keyboards.utils import *

from database.models import Subscription
from database.models.admin import Tournament, Discipline, Region


def languages():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data="select_lang:ru")
    builder.button(text="🇺🇿 O`zbekcha", callback_data="select_lang:uz")
    return builder.adjust(1).as_markup()


def subscription(l10n: FluentLocalization, subscriptions: List[Subscription]):
    builder = InlineKeyboardBuilder()
    for i in subscriptions:
        builder.button(
            text=i.title,
            url=i.url,
        )
    builder.button(
        text=l10n.format_value("im-subscribed"), callback_data="check-subscriptions"
    )
    return builder.adjust(
        *[*[2 for _ in range(len(subscriptions) // 2)], 1]
    ).as_markup()


def tournaments_list(tournaments: List[Tournament]):
    builder = InlineKeyboardBuilder()
    data = RegCallback(action='select-tournament')
    for i in tournaments:
        data.tournament_id = i.id
        builder.button(
            text=i.name,
            callback_data=data.pack()
        )
    return builder.adjust(1).as_markup()


def register_to_tournament(data: RegCallback, l10n: FluentLocalization):
    builder = InlineKeyboardBuilder()
    data.action = 'register'
    builder.button(
        text=l10n.format_value('b-register-to-tournament'),
        callback_data=data.pack()
    )
    data.action = 'main'
    builder.button(
        text=l10n.format_value('back'),
        callback_data=data.pack()
    )
    return builder.adjust(1).as_markup()


def select_discipline(data: RegCallback, l10n: FluentLocalization, disciplines: list[Discipline]):
    builder = InlineKeyboardBuilder()
    data.action = 'select-discipline'
    for i in disciplines:
        data.discipline_id = i.id
        builder.button(
            text=i.name,
            callback_data=data.pack()
        )
    sizes = generate_sizes([], disciplines, 2, 10, 1)
    data.action = 'select-tournament'
    builder.button(
        text=l10n.format_value('back'),
        callback_data=data.pack()
    )
    sizes.append(1)
    return builder.adjust(*sizes).as_markup()


def select_region(data: RegCallback, l10n: FluentLocalization, regions: list[Region]):
    builder = InlineKeyboardBuilder()
    data.action = 'select-region'
    for i in regions:
        data.region_id = i.id
        builder.button(
            text=i.name,
            callback_data=data.pack()
        )
    sizes = generate_sizes([], regions, 2, 10, 1)
    data.action = 'register'
    builder.button(
        text=l10n.format_value('back'),
        callback_data=data.pack()
    )
    sizes.append(1)
    return builder.adjust(*sizes).as_markup()


def select_gender(data: RegCallback, l10n: FluentLocalization):
    builder = InlineKeyboardBuilder()
    data.action = 'gender-1'
    builder.button(
        text=l10n.format_value('b-male'),
        callback_data=data.pack()
    )
    data.action = 'gender-0'
    builder.button(
        text=l10n.format_value('b-female'),
        callback_data=data.pack()
    )
    data.action = 'select-region'
    builder.button(
        text=l10n.format_value('back'),
        callback_data=data.pack()
    )
    return builder.adjust(1).as_markup()


def select_weight(data: RegCallback, l10n: FluentLocalization):
    builder = InlineKeyboardBuilder()
    for i in [
        "21 kg", "24 kg", "27 kg",
        "30 kg", "33 kg", "35 kg",
        "38 kg", "41 kg", "44 kg",
        "48 kg", "52 kg", "+52 kg",
        "53 kg", "57 kg", "58 kg",
        "62 kg", "64 kg", "67 kg",
        "+67 kg", "+70 kg", "73 kg",
        "80 kg", "88 kg", "93 kg",
        "+97 kg",
    ]:
        data.action = f'weight-{i}'
        builder.button(
            text=i,
            callback_data=data.pack()
        )
    sizes = [3] * 8
    sizes.append(1)
    data.action = 'select-region'
    builder.button(
        text=l10n.format_value('back'),
        callback_data=data.pack()
    )
    sizes.append(1)
    return builder.adjust(*sizes).as_markup()


def confirm_registration(data: RegCallback, l10n: FluentLocalization):
    builder = InlineKeyboardBuilder()
    data.action = 'confirm'
    builder.button(
        text=l10n.format_value('b-correct'),
        callback_data=data.pack()
    )
    data.action = 'main'
    builder.button(
        text=l10n.format_value('b-restart'),
        callback_data=data.pack()
    )
    return builder.adjust(2).as_markup()
