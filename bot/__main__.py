import asyncio
from collections.abc import Awaitable
from typing import Callable

import orjson
import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import AsyncContainer, make_async_container

import nats
from bot.config import BotConfig
from bot.handling import schema
from bot.nats_storage import NATSFSMStorage
from nats.js.kv import KeyValue


def bot_factory(config: BotConfig) -> Bot:
    return Bot(
        config.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


async def dispatcher_factory(kv_states: KeyValue, kv_data: KeyValue) -> Dispatcher:
    return Dispatcher(
        storage=NATSFSMStorage(
            kv_states,
            kv_data,
            serializer=orjson.dumps,
            deserializer=orjson.loads,
        ),
    )


def dishka_container_factory() -> AsyncContainer:
    from bot.core.providers import get_providers

    return make_async_container(*get_providers())


async def main(
    config: BotConfig,
    nats_address: str,
    _bot_factory: Callable[[BotConfig], Bot] = bot_factory,
    _dispatcher_factory: Callable[
        [KeyValue, KeyValue],
        Awaitable[Dispatcher],
    ] = dispatcher_factory,
    _di_container_factory: Callable[[], AsyncContainer] = dishka_container_factory,
) -> None:
    logger = structlog.get_logger(__name__)

    nc = await nats.connect(nats_address)
    js = nc.jetstream()
    await logger.debug("NATS connection established")

    bot = _bot_factory(config)
    kv_states = await js.key_value(config.fsm.states_bucket)
    kv_data = await js.key_value(config.fsm.data_bucket)
    await logger.debug("Bot and KV FSM buckets initialized")

    dp = await schema.assemble(
        _dispatcher_factory(kv_states, kv_data),
        _di_container_factory(),
    )

    bot_representation = await bot.me()
    await logger.info(f"Bot {bot_representation.first_name} is ready to serve requests")
    try:
        await asyncio.gather(
            dp.start_polling(bot),
        )
    finally:
        await nc.close()
