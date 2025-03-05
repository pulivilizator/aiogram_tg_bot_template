from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.fsm.state import State
from aiogram.types import TelegramObject, Update
from aiogram_dialog import StartMode
from aiogram_dialog.api.exceptions import UnknownIntent
from structlog import get_logger


class DialogResetMiddleware(BaseMiddleware):
    def __init__(self, init_state: State, mode: StartMode) -> None:
        self.init_state = init_state
        self.mode = mode
        self.logger = get_logger(self.__class__.__name__)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> None:
        await self.logger.debug("DialogResetMiddleware begun")
        try:
            await handler(event, data)
        except UnknownIntent:
            await self.logger.info(f"Unknown intent {type(data)}")
            manager = data.get("dialog_manager")
            if manager:
                await manager.start(self.init_state, mode=self.mode)
            if event.callback_query is not None:
                await event.callback_query.answer()
        await self.logger.debug("DialogResetMiddleware end")
