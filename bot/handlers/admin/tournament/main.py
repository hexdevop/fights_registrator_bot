from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from sqlalchemy import select, func
from sqlalchemy.orm import load_only

from bot.keyboards.admin import inline
from bot.keyboards.admin.factory import TournamentCallbackData
from database import get_slave_session
from database.models.admin import Tournament

router = Router()


@router.message(F.text == "Турниры 💪")
async def tournaments_list(
    message: types.Message,
    state: FSMContext,
    l10n: FluentLocalization,
    page: int = 1,
    edit: bool = False,
):
    await state.clear()
    async with get_slave_session() as session:
        tournaments = (
            await session.scalars(
                select(Tournament)
                .options(load_only(Tournament.id, Tournament.name))
                .offset((page - 1) * 10)
                .limit(10)
            )
        ).all()
        tournaments_count = await session.scalar(select(func.count(Tournament.id)))
    method = message.edit_text if edit else message.answer
    await method(
        text=l10n.format_value("tournament-list"),
        reply_markup=inline.tournament_list(tournaments, tournaments_count, page),
    )


@router.callback_query(TournamentCallbackData.filter(F.action.in_({"main", "page"})))
async def back_to_main_and_pagination(
    call: types.CallbackQuery,
    callback_data: TournamentCallbackData,
    state: FSMContext,
    l10n: FluentLocalization,
):
    await tournaments_list(call.message, state, l10n, callback_data.page, edit=True)
