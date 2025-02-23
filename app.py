import asyncio

import structlog

import logs
from bot import bot
from config import Config, parse_config

async def main() -> None:
    config: Config = parse_config()
    logs.startup(config.logging)
    logger = structlog.get_logger(__name__)
    await logger.info('App is starting, configs parsed successfully')
    try:
        await asyncio.gather(
            bot(
                config.bot,
                nats_address=config.nats.dsn.unicode_string(),
            ),
        )
    except SystemExit:
        await logger.info('System shutdown')
    except KeyboardInterrupt:
        await logger.info('Shutdown by external call ( KeyboardInterrupt )')
    except Exception as e:
        await logger.exception('Abnormal shutdown detected, critical error happened', e)

if __name__ == '__main__':
    asyncio.run(main())