from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from bot.handlers.admin.tournament.main import tournaments_list
from bot.keyboards.admin import inline
from bot.keyboards.admin.factory import TournamentCallbackData
from bot.states import TournamentState
from bot.utils import helper
from database import get_master_session
from database.models.admin import Tournament

router = Router()


@router.callback_query(TournamentCallbackData.filter(F.action == "add"))
async def add_tournament(
    call: types.CallbackQuery,
    callback_data: TournamentCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await state.update_data(callback_data=callback_data.model_dump())
    message_id = (
        await call.message.edit_text(
            text=l10n.format_value("get-tournament-name"),
            reply_markup=inline.cancel(callback_data, "main"),
        )
    ).message_id
    await state.update_data(message_id=message_id)
    await state.set_state(TournamentState.name)


@router.message(TournamentState.name, F.text)
async def get_tournament_name(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = TournamentCallbackData.model_validate(data.get("callback_data"))
    message_id = (
        await message.answer(
            text=l10n.format_value("get-tournament-organizer"),
            reply_markup=inline.cancel(callback_data, "main"),
        )
    ).message_id
    await state.update_data(name=message.text)
    await state.update_data(message_id=message_id)
    await state.set_state(TournamentState.organizer)


@router.message(TournamentState.organizer, F.text)
async def get_tournament_organizer(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = TournamentCallbackData.model_validate(data.get("callback_data"))
    message_id = (
        await message.answer(
            text=l10n.format_value("get-tournament-date"),
            reply_markup=inline.cancel(callback_data, "main"),
        )
    ).message_id
    await state.update_data(organizer=message.text)
    await state.update_data(message_id=message_id)
    await state.set_state(TournamentState.date)


@router.message(TournamentState.date, F.text)
async def get_tournament_date(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = TournamentCallbackData.model_validate(data.get("callback_data"))
    date = message.text
    args = date.split(".")
    if "." in date and len(args) == 3 and len([i for i in args if i.isdigit()]) == 3:
        message_id = (
            await message.answer(
                text=l10n.format_value("get-tournament-age"),
                reply_markup=inline.cancel(callback_data, "main"),
            )
        ).message_id
        await state.update_data(date=message.text)
        await state.update_data(message_id=message_id)
        await state.set_state(TournamentState.age)
    else:
        message_id = (
            await message.answer(
                text=l10n.format_value("get-tournament-date"),
                reply_markup=inline.cancel(callback_data, "main"),
            )
        ).message_id
        await state.update_data(message_id=message_id)


@router.message(TournamentState.age, F.text)
async def get_tournament_age(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = TournamentCallbackData.model_validate(data.get("callback_data"))
    date = message.text
    args = date.split("-")
    if "-" in date and len(args) == 2 and len([i for i in args if i.isdigit()]) == 2:
        async with get_master_session() as session:
            async with session.begin():
                session.add(
                    Tournament(
                        name=data.get("name"),
                        organizer=data.get("organizer"),
                        date=data.get("date"),
                        age=message.text,
                    )
                )
        await message.answer(text=l10n.format_value("tournament-added"))
        await tournaments_list(message, state, l10n, callback_data.page)
    else:
        message_id = (
            await message.answer(
                text=l10n.format_value("get-tournament-date"),
                reply_markup=inline.cancel(callback_data, "main"),
            )
        ).message_id
        await state.update_data(message_id=message_id)
