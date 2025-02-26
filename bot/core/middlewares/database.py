from collections.abc import Awaitable
from typing import Any, Callable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from .inject import aiogram_middleware_inject


class DatabaseMiddleware(BaseMiddleware):
    def __init__(
        self,
    ) -> None:
        self.logger = structlog.getLogger()

    @aiogram_middleware_inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
        session: FromDishka[AsyncSession],
    ) -> None:
        try:
            await handler(event, data)
            await session.commit()
        except Exception as e:
            await self.logger.error("Error during database session", exc_info=e)
            await session.rollback()
            raise e
