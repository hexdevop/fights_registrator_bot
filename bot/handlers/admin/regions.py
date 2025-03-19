from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from sqlalchemy import select, func, delete

from bot.keyboards.admin import inline
from bot.keyboards.admin.factory import RegionCallbackData
from bot.states import RegionState
from bot.utils import helper
from database import get_slave_session, get_master_session
from database.models import User
from database.models.admin import Region

router = Router()



@router.message(F.text == 'Регионы 🏳️')
async def regions_list(
        message: types.Message,
        state: FSMContext,
        l10n: FluentLocalization,
        page: int = 1,
        edit: bool = False,
):
    await state.clear()
    async with get_slave_session() as session:
        regions = (await session.scalars(
            select(Region).offset((page - 1) * 10).limit(10)
        )).all()
        regions_count = await session.scalar(
            select(func.count(Region.id))
        )
    method = message.edit_text if edit else message.answer
    await method(
        text=l10n.format_value('regions-list'),
        reply_markup=inline.regions_list(regions, regions_count, page)
    )


@router.callback_query(RegionCallbackData.filter(F.action.in_({'page', 'main'})))
async def back_to_main_or_pagination(
        call: types.CallbackQuery,
        callback_data: RegionCallbackData,
        state: FSMContext,
        l10n: FluentLocalization,
):
    await regions_list(call.message, state, l10n, callback_data.page, edit=True)


@router.callback_query(RegionCallbackData.filter(F.action == 'add'))
async def add_region(
        call: types.CallbackQuery,
        callback_data: RegionCallbackData,
        state: FSMContext,
        l10n: FluentLocalization,
):
    await state.update_data(callback_data=callback_data.model_dump())
    message_id = (
        await call.message.edit_text(
            text=l10n.format_value('get-region-name'),
            reply_markup=inline.cancel(callback_data, 'main')
        )
    ).message_id
    await state.update_data(message_id=message_id)
    await state.set_state(RegionState.name)


@router.message(RegionState.name, F.text)
async def get_region_name(
        message: types.Message,
        state: FSMContext,
        l10n: FluentLocalization,
):
    data = await state.get_data()
    await helper.delete_messages(message, data)
    callback_data = RegionCallbackData.model_validate(data.get('callback_data'))
    async with get_master_session() as session:
        async with session.begin():
            region_exist = await session.scalar(select(func.count(Region.id)).where(Region.name == message.text))
            if region_exist:
                message_id = (
                    await message.answer(
                        text=l10n.format_value('this-region-exist'),
                        reply_markup=inline.cancel(callback_data, 'main')
                    )
                ).message_id
                return await state.update_data(message_id=message_id)
            session.add(Region(name=message.text.lower().capitalize()))
    await message.answer(text=l10n.format_value('region-added', {'name': message.text.lower().capitalize()}))
    await regions_list(message, state, l10n)


@router.callback_query(RegionCallbackData.filter(F.action == 'delete'))
async def delete_region(
        call: types.CallbackQuery,
        callback_data: RegionCallbackData,
        l10n: FluentLocalization,
):
    async with get_slave_session() as session:
        name = await session.scalar(
            select(Region.name).where(Region.id == callback_data.id)
        )
    await call.message.edit_text(
        text=l10n.format_value('confirm-deleting-region', {'name': name}),
        reply_markup=inline.confirm(callback_data, 'confirm-delete', 'main')
    )


@router.callback_query(RegionCallbackData.filter(F.action == 'confirm-delete'))
async def confirm_delete_region(
        call: types.CallbackQuery,
        callback_data: RegionCallbackData,
        state: FSMContext,
        l10n: FluentLocalization,
):
    async with get_master_session() as session:
        async with session.begin():
            name = await session.scalar(
                select(Region.name).where(Region.id == callback_data.id)
            )
            await session.execute(
                delete(User).where(User.region_id == callback_data.id)
            )
            await session.execute(
                delete(Region).where(Region.id == callback_data.id)
            )
    await call.message.edit_text(
        text=l10n.format_value('region-deleted', {'name': name})
    )
    await regions_list(call.message, state, l10n, callback_data.page)



@router.callback_query(RegionCallbackData.filter(F.action == 'ok'))
async def ok(call: types.CallbackQuery):
    await call.answer()
