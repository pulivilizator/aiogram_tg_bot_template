from collections.abc import Awaitable

import structlog
from aiogram import Dispatcher
from aiogram_dialog import StartMode, setup_dialogs
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from bot.core.middlewares import (
    DatabaseMiddleware,
    DialogResetMiddleware,
    LoggingMiddleware,
    RegisterMiddleware,
    TranslatorRunnerMiddleware,
)
from bot.handling.dialogs import get_dialogs
from bot.handling.handlers import get_routers
from bot.handling.states.main_menu import MainMenuSG

logger = structlog.getLogger("schema")


async def assemble(
    dispatcher_factory: Awaitable[Dispatcher],
    di_container: AsyncContainer,
) -> Dispatcher:
    dp = await dispatcher_factory
    container = di_container
    setup_dishka(container, dp, auto_inject=True)
    setup_dialogs(dp)
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(DatabaseMiddleware())
    dp.update.middleware(RegisterMiddleware())
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.update.middleware(
        DialogResetMiddleware(init_state=MainMenuSG.menu, mode=StartMode.RESET_STACK),
    )
    dp.include_routers(*get_routers(), *get_dialogs())
    return dp
