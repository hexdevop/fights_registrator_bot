from aiogram.filters.callback_data import CallbackData


class SubscriptionCallbackData(CallbackData, prefix="s"):
    action: str
    id: int = 0

    page: int


class TournamentCallbackData(CallbackData, prefix="t"):
    action: str
    id: int = 0

    discipline_id: int = 0

    page: int = 1


class RegionCallbackData(CallbackData, prefix="r"):
    action: str
    id: int = 0

    page: int = 1
