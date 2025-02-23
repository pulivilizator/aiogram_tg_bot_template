from typing import Awaitable

import structlog
from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka

from bot.handling.dialogs import get_dialogs
from bot.handling.handlers import get_routers
from bot.infrastructure.dishka_container import make_dishka_container

logger = structlog.getLogger('schema')


async def assemble(
        dispatcher_factory: Awaitable[Dispatcher]
) -> Dispatcher:
    dp = await dispatcher_factory
    container = make_dishka_container()
    setup_dishka(container, dp, auto_inject=True)
    setup_dialogs(dp)
    dp.include_routers(*get_routers(), *get_dialogs())
    return dp