import asyncio
import os

import structlog

import nats
from nats.js.api import KeyValueConfig


async def main():
    logger = structlog.get_logger(__name__)
    nc = await nats.connect(os.getenv("NATS_URL"))
    js = nc.jetstream()

    logger.debug("NATS соединение установлено")

    await js.create_key_value(KeyValueConfig("fsm_data_aiogram"))
    await js.create_key_value(KeyValueConfig("fsm_states_aiogram"))


if __name__ == "__main__":
    asyncio.run(main())
