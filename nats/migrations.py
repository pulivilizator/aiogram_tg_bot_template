import asyncio
import os

import structlog

import nats
from nats.js.api import KeyValueConfig


async def main() -> None:
    logger = structlog.get_logger(__name__)
    nc_url = os.getenv("NATS_URL")
    if not nc_url:
        raise ValueError("NATS_URL environment variable not set")
    nc = await nats.connect(nc_url)
    js = nc.jetstream()

    logger.debug("NATS connection established")

    await js.create_key_value(KeyValueConfig("fsm_data_aiogram"))
    await js.create_key_value(KeyValueConfig("fsm_states_aiogram"))


if __name__ == "__main__":
    asyncio.run(main())
