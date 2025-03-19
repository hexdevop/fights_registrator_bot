from aiogram.filters.callback_data import CallbackData


class RegCallback(CallbackData, prefix='reg'):
    action: str
    tournament_id: int = 0
    discipline_id: int = 0
    region_id: int = 0
