from typing import AsyncIterator

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import TelegramObject
from aiohttp import ClientSession
from dishka import Provider, provide, Scope, from_context
from fluentogram import TranslatorHub
from orjson import orjson
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from config import Config, parse_config
from i18n.factory import i18n_factory


class CommonProvider(Provider):
    event = from_context(provides=TelegramObject, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return parse_config()

    @provide(scope=Scope.APP)
    async def get_redis(self, config: Config) -> AsyncIterator[Redis]:
        r = Redis.from_url(config.redis.dsn.unicode_string())
        yield r
        await r.close()

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, config: Config) -> async_sessionmaker:
        engine = create_async_engine(url=config.db.uri,
                                     pool_size=config.db.pool_size,
                                     max_overflow=config.db.max_overflow)
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=True, class_=AsyncSession)

    @provide(scope=Scope.REQUEST)
    async def get_db_session(self, sessionmaker: async_sessionmaker) -> AsyncIterator[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_translator_hub(self) -> TranslatorHub:
        translator_hub = i18n_factory()
        return translator_hub

    @provide(scope=Scope.REQUEST)
    async def get_http_session(self) -> ClientSession:
        return await AiohttpSession(
            json_dumps=lambda data: orjson.dumps(data).decode(),
            json_loads=orjson.loads,
        ).create_session()