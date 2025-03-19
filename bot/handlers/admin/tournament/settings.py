from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from sqlalchemy import select, update, case, delete

from bot.handlers.admin.tournament.main import tournaments_list
from bot.keyboards.admin import inline
from bot.keyboards.admin.factory import TournamentCallbackData
from database import get_slave_session, get_master_session
from database.models import User
from database.models.admin import Tournament, Discipline

router = Router()


@router.callback_query(TournamentCallbackData.filter(F.action == "settings"))
async def tournament_settings(
    event: types.CallbackQuery | types.Message,
    callback_data: TournamentCallbackData,
    l10n: FluentLocalization,
):
    async with get_slave_session() as session:
        tournament = await session.scalar(
            select(Tournament).where(Tournament.id == callback_data.id)
        )
        disciplines = (
            await session.scalars(
                select(Discipline.name).where(
                    Discipline.tournament_id == callback_data.id
                )
            )
        ).all()
    method = (
        event.answer if isinstance(event, types.Message) else event.message.edit_text
    )
    await method(
        text=l10n.format_value(
            "tournament-settings",
            {
                "name": tournament.name,
                "organizer": tournament.organizer,
                "status": tournament.status.name,
                "date": tournament.date,
                "age": tournament.age,
                "disciplines": (
                    ", ".join(disciplines) if disciplines else l10n.format_value("null")
                ),
            },
        ),
        reply_markup=inline.tournament_settings(callback_data, tournament.status),
    )


@router.callback_query(TournamentCallbackData.filter(F.action == "status"))
async def change_status(
    call: types.CallbackQuery,
    callback_data: TournamentCallbackData,
    l10n: FluentLocalization,
):
    async with get_master_session() as session:
        async with session.begin():
            await session.execute(
                update(Tournament)
                .where(Tournament.id == callback_data.id)
                .values(
                    status=case(
                        (Tournament.status == "AVAILABLE", "STOPPED"), else_="AVAILABLE"
                    )
                )
            )
    await tournament_settings(call, callback_data, l10n)


@router.callback_query(TournamentCallbackData.filter(F.action == "delete"))
async def delete_tournament(
    call: types.CallbackQuery,
    callback_data: TournamentCallbackData,
    l10n: FluentLocalization,
):
    await call.message.edit_text(
        text=l10n.format_value("confirm-deleting-tournament"),
        reply_markup=inline.confirm(callback_data, "confirm-delete", "settings"),
    )


@router.callback_query(TournamentCallbackData.filter(F.action == "confirm-delete"))
async def confirm_deleting(
    call: types.CallbackQuery,
    callback_data: TournamentCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    async with get_master_session() as session:
        async with session.begin():
            await session.execute(User).where(User.tournament_id == callback_data.id)
            await session.execute(
                delete(Discipline).where(Discipline.tournament_id == callback_data.id)
            )
            await session.execute(
                delete(Tournament).where(Tournament.id == callback_data.id)
            )
    await tournaments_list(call.message, state, l10n, callback_data.page, edit=True)
