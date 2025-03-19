from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from sqlalchemy import select, delete
from sqlalchemy.orm import load_only

from bot.keyboards.admin import inline
from bot.keyboards.admin.factory import TournamentCallbackData
from bot.states import TournamentState
from bot.utils import helper
from database import get_slave_session, get_master_session
from database.models import User
from database.models.admin import Discipline

router = Router()


@router.callback_query(TournamentCallbackData.filter(F.action == "disciplines"))
async def disciplines_list(
    event: types.CallbackQuery | types.Message,
    callback_data: TournamentCallbackData,
    l10n: FluentLocalization,
):
    async with get_slave_session() as session:
        disciplines = (
            await session.scalars(
                select(Discipline)
                .options(load_only(Discipline.id, Discipline.name))
                .where(Discipline.tournament_id == callback_data.id)
            )
        ).all()
    method = (
        event.answer if isinstance(event, types.Message) else event.message.edit_text
    )
    await method(
        text=l10n.format_value("discipline-list"),
        reply_markup=inline.disciplines_list(callback_data, disciplines),
    )


@router.callback_query(TournamentCallbackData.filter(F.action == "add-discipline"))
async def add_discipline(
    call: types.CallbackQuery,
    callback_data: TournamentCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await state.update_data(callback_data=callback_data.model_dump())
    message_id = (
        await call.message.edit_text(
            text=l10n.format_value("get-discipline-name"),
            reply_markup=inline.cancel(callback_data, "disciplines"),
        )
    ).message_id
    await state.update_data(message_id=message_id)
    await state.set_state(TournamentState.discipline)


@router.message(TournamentState.discipline, F.text)
async def get_discipline_name(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = TournamentCallbackData.model_validate(data.get("callback_data"))
    async with get_master_session() as session:
        async with session.begin():
            session.add(Discipline(name=message.text, tournament_id=callback_data.id))
    await state.clear()
    await disciplines_list(message, callback_data, l10n)


@router.callback_query(TournamentCallbackData.filter(F.action == "delete-discipline"))
async def delete_discipline(
    call: types.CallbackQuery,
    callback_data: TournamentCallbackData,
    l10n: FluentLocalization,
):
    await call.message.edit_text(
        text=l10n.format_value("confirm-deleting-discipline"),
        reply_markup=inline.confirm(
            callback_data, "confirm-del-discipline", "disciplines"
        ),
    )


@router.callback_query(TournamentCallbackData.filter(F.action == "confirm-del-discipline"))
async def confirm_deleting_discipline(
    call: types.CallbackQuery,
    callback_data: TournamentCallbackData,
    l10n: FluentLocalization,
):
    async with get_master_session() as session:
        async with session.begin():
            await session.execute(
                delete(User).where(User.discipline_id == callback_data.discipline_id)
            )
            await session.execute(
                delete(Discipline).where(Discipline.id == callback_data.discipline_id)
            )
    await disciplines_list(call, callback_data, l10n)


@router.callback_query(TournamentCallbackData.filter(F.action == "ok"))
async def ok(call: types.CallbackQuery):
    await call.answer()
