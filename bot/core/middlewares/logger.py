from collections.abc import Awaitable
from datetime import datetime
from typing import Any, Callable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = structlog.get_logger(self.__class__.__name__)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> None:
        start_time = datetime.now()
        structlog.contextvars.bind_contextvars(
            update=event.model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude_defaults=True,
            ),
            start_time=datetime.now(),
        )
        try:
            await handler(event, data)
        except Exception as e:  # noqa #BLE001
            end_time = datetime.now()
            await self.logger.exception(
                "Abnormal handling event detected, critical error happened",
                e,
                start_time=start_time,
                end_time=end_time,
                execution_time=(end_time - start_time).microseconds,
            )
        else:
            end_time = datetime.now()
            execution_time = end_time - start_time
            await self.logger.info(
                f"Event successfully executed in {execution_time.microseconds} microseconds",  # noqa#E501
                execution_time=execution_time,
            )
        finally:
            structlog.contextvars.clear_contextvars()
