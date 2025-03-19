import datetime

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from sqlalchemy import select
from sqlalchemy.orm import load_only

from bot.enums import Status
from bot.filters.buttons import Button
from bot.keyboards.user import inline
from bot.keyboards.user.factory import RegCallback
from bot.states import RegState
from bot.utils import helper
from database import get_slave_session, get_master_session
from database.models import User
from database.models.admin import Tournament, Discipline, Region

router = Router()


@router.message(Button("register"))
async def registration_menu(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
    edit: bool = False,
):
    await state.clear()
    async with get_slave_session() as session:
        tournaments = (
            await session.scalars(
                select(Tournament).options(load_only(Tournament.id, Tournament.name))
            )
        ).all()
    method = message.edit_text if edit else message.answer
    await method(
        text=l10n.format_value("select-tournament"),
        reply_markup=inline.tournaments_list(tournaments),
    )


@router.callback_query(RegCallback.filter(F.action == "main"))
async def back_to_main(
    call: types.CallbackQuery,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await registration_menu(call.message, state, l10n, edit=True)


@router.callback_query(RegCallback.filter(F.action == "select-tournament"))
async def select_tournament(
    call: types.CallbackQuery,
    callback_data: RegCallback,
    l10n: FluentLocalization,
):
    async with get_slave_session() as session:
        tournament = await session.scalar(
            select(Tournament).where(Tournament.id == callback_data.tournament_id)
        )
    await call.message.edit_text(
        text=l10n.format_value(
            "tournament-info",
            {
                "name": tournament.name,
                "date": tournament.date,
                "organizer": tournament.organizer,
                "age": tournament.age,
            },
        ),
        reply_markup=inline.register_to_tournament(callback_data, l10n),
    )


@router.callback_query(RegCallback.filter(F.action == "register"))
async def start_registration(
    call: types.CallbackQuery,
    callback_data: RegCallback,
    l10n: FluentLocalization,
):
    async with get_slave_session() as session:
        status = await session.scalar(
            select(Tournament.status).where(Tournament.id == callback_data.tournament_id)
        )
        if status == Status.STOPPED:
            return await call.answer(text=l10n.format_value('tournament-stopped'), show_alert=True)
        disciplines = (
            await session.scalars(
                select(Discipline)
                .options(load_only(Discipline.id, Discipline.name))
                .where(Discipline.tournament_id == callback_data.tournament_id)
            )
        ).all()
    await call.message.edit_text(
        text=l10n.format_value("select-discipline"),
        reply_markup=inline.select_discipline(callback_data, l10n, disciplines),
    )


@router.callback_query(RegCallback.filter(F.action == "select-discipline"))
async def select_discipline(
    call: types.CallbackQuery,
    callback_data: RegCallback,
    l10n: FluentLocalization,
):
    async with get_slave_session() as session:
        regions = (await session.scalars(select(Region))).all()
    await call.message.edit_text(
        text=l10n.format_value("select-region"),
        reply_markup=inline.select_region(callback_data, l10n, regions),
    )


@router.callback_query(RegCallback.filter(F.action == "select-region"))
async def select_region(
    call: types.CallbackQuery,
    callback_data: RegCallback,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await state.update_data(callback_data=callback_data.model_dump())
    message_id = (
        await call.message.edit_text(
            text=l10n.format_value("get-initials"),
            reply_markup=inline.cancel(callback_data, "register"),
        )
    ).message_id
    await state.update_data(message_id=message_id)
    await state.set_state(RegState.initials)


@router.message(RegState.initials, F.text)
async def get_initials(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = RegCallback.model_validate(data.get("callback_data"))
    initials = message.text
    if len(initials.split()) != 3 or helper.has_cyrillic(initials):
        message_id = (
            await message.answer(
                text=l10n.format_value("get-initials"),
                reply_markup=inline.cancel(callback_data, "select-region"),
            )
        ).message_id
        return await state.update_data(message_id=message_id)
    await state.update_data(initials=message.text)
    message_id = (
        await message.answer(
            text=l10n.format_value("get-coach-initials"),
            reply_markup=inline.cancel(callback_data, "select-region"),
        )
    ).message_id
    await state.update_data(message_id=message_id)
    await state.set_state(RegState.coach_initials)


@router.message(RegState.coach_initials, F.text)
async def get_coach_initials(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = RegCallback.model_validate(data.get("callback_data"))
    coach_initials = message.text
    if len(coach_initials.split()) != 3 or helper.has_cyrillic(coach_initials):
        message_id = (
            await message.answer(
                text=l10n.format_value("get-coach-initials"),
                reply_markup=inline.cancel(callback_data, "select-region"),
            )
        ).message_id
        return await state.update_data(message_id=message_id)
    await state.update_data(coach_initials=message.text)
    message_id = (
        await message.answer(
            text=l10n.format_value("get-age"),
            reply_markup=inline.cancel(callback_data, "select-region"),
        )
    ).message_id
    await state.update_data(message_id=message_id)
    await state.set_state(RegState.age)


@router.message(RegState.age, F.text)
async def get_age(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = RegCallback.model_validate(data.get("callback_data"))
    try:
        date = validate_date(message.text)
    except ValueError:
        message_id = (
            await message.answer(
                text=l10n.format_value("incorrect-age"),
                reply_markup=inline.cancel(callback_data, "select-region"),
            )
        ).message_id
        return await state.update_data(message_id=message_id)
    if date is False:
        message_id = (
            await message.answer(
                text=l10n.format_value("incorrect-age"),
                reply_markup=inline.cancel(callback_data, "select-region"),
            )
        ).message_id
        return await state.update_data(message_id=message_id)
    async with get_slave_session() as session:
        limit = await session.scalar(
            select(Tournament.age).where(Tournament.id == callback_data.tournament_id)
        )
    age = calculate_age(date)
    min_limit, max_limit = limit.split("-")
    if not int(min_limit) <= age <= int(max_limit):
        await message.answer(
            text=l10n.format_value(
                "age-limit", {"min_age": min_limit, "max_age": max_limit}
            )
        )
        return await state.clear()
    await state.update_data(date=message.text)
    message_id = (
        await message.answer(
            text=l10n.format_value("select-gender"),
            reply_markup=inline.select_gender(callback_data, l10n),
        )
    ).message_id
    await state.update_data(message_id=message_id)
    await state.set_state(RegState.gender)


@router.callback_query(RegCallback.filter(F.action.startswith("gender")))
async def select_gender(
    call: types.CallbackQuery,
    callback_data: RegCallback,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await state.update_data(gender=callback_data.action.split("-")[1])
    await call.message.edit_text(
        text=l10n.format_value("select-weight"),
        reply_markup=inline.select_weight(callback_data, l10n),
    )


@router.callback_query(RegCallback.filter(F.action.startswith("weight")))
async def select_weight(
    call: types.CallbackQuery,
    callback_data: RegCallback,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await state.update_data(weight=callback_data.action.split("-")[1])
    async with get_slave_session() as session:
        tournament = await session.scalar(
            select(Tournament.name).where(Tournament.id == callback_data.tournament_id)
        )
        discipline = await session.scalar(
            select(Discipline.name).where(Discipline.id == callback_data.discipline_id)
        )
        region = await session.scalar(
            select(Region.name).where(Region.id == callback_data.region_id)
        )
    data = await state.get_data()
    await call.message.edit_text(
        text=l10n.format_value(
            "confirm-registration",
            {
                'tournament': tournament,
                'discipline': discipline,
                'region': region,
                'initials': data.get('initials'),
                'coach_initials': data.get('coach_initials'),
                'date': data.get('date'),
                'gender': data.get('gender'),
                'weight': data.get('weight'),
            }
        ),
        reply_markup=inline.confirm_registration(callback_data, l10n),
    )


@router.callback_query(RegCallback.filter(F.action == 'confirm'))
async def confirm_registration(
        call: types.CallbackQuery,
        callback_data: RegCallback,
        state: FSMContext,
        l10n: FluentLocalization,
):
    data = await state.get_data()
    async with get_master_session() as session:
        async with session.begin():
            session.add(
                User(
                    user_id=call.from_user.id,
                    username=call.from_user.username,
                    lang_code=call.from_user.language_code,
                    tournament_id=callback_data.tournament_id,
                    discipline_id=callback_data.discipline_id,
                    region_id=callback_data.region_id,
                    initials=data.get('initials'),
                    coach_initials=data.get('coach_initials'),
                    date=validate_date(data.get('date')),
                    gender=int(data.get('gender')),
                    weight=data.get('weight'),
                     )
            )
    await call.message.edit_text(
        text=l10n.format_value('you-was-registered'),
    )
    await state.clear()


def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> datetime.date:
    birth_date = datetime.datetime.strptime(date_str, date_format).date()
    if birth_date > datetime.date.today():
        return False
    return birth_date


def calculate_age(birth_date: datetime.date) -> int:
    today = datetime.date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age
