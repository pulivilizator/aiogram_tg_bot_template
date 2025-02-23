from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.middlewares import aiogram_middleware_inject


class DatabaseMiddleware(BaseMiddleware):

    def __init__(
            self,
    ) -> None:
        self.logger = structlog.getLogger()

    @aiogram_middleware_inject
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
            session: FromDishka[AsyncSession]
    ) -> None:
        try:
            await handler(event, data)
            await session.commit()
        except Exception as e:
            await self.logger.error("Error during database session", exc_info=e)
            await session.rollback()
            raise e

