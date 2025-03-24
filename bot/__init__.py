from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from bot.services import Cache
from bot.utils import fluent_loader
from config import config

bot = Bot(
    token=config.bot.token,
    session=AiohttpSession(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML, protect_content=False, link_preview_is_disabled=True
    ),
)

storage = RedisStorage(Redis(host=config.redis.host, db=config.redis.state))

languages = fluent_loader.get_fluent_localization(languages=['ru', 'uz'])

cache = Cache(Redis(host=config.redis.host, db=config.redis.cache), languages)

dp = Dispatcher(
    storage=storage,
    cache=cache,
    languages=languages,
    config=config,
)
