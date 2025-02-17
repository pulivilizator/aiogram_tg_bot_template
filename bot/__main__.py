from aiogram import Dispatcher, Bot
from orjson import orjson

from bot.nats_storage import NATSFSMStorage


def bot_factory(config: BotConfig) -> Bot:
    return Bot(
        config.token.get_secret_value(),
        session=AiohttpSession(
            json_dumps=lambda data: orjson.dumps(data).decode(),
            json_loads=orjson.loads,
        ),
    )


async def dispatcher_factory(kv_states: KeyValue, kv_data: KeyValue) -> Dispatcher:
    return Dispatcher(
        storage=NATSFSMStorage(
            kv_states, kv_data, serializer=orjson.dumps, deserializer=orjson.loads
        )
    )