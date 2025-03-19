from aiogram.fsm.state import StatesGroup, State


class SubscriptionState(StatesGroup):
    url = State()
    message_from_channel = State()
    channel_link = State()


class TournamentState(StatesGroup):
    name = State()
    organizer = State()
    date = State()
    age = State()

    discipline = State()


class RegionState(StatesGroup):
    name = State()

class RegState(StatesGroup):
    initials = State()
    coach_initials = State()
    age = State()
    gender = State()
    weight = State()
