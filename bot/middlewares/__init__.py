from aiogram import Dispatcher

from .callback_answer import CallbackAnswer
from .subscription import SubscriptionMiddleware
from .language import LanguageMiddleware


def setup(dp: Dispatcher):
    dp.update.middleware(LanguageMiddleware())

    dp.callback_query.middleware(CallbackAnswer())
