from typing import Callable, Any, Awaitable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import User, TelegramObject, Message
from dishka.integrations.aiogram import FromDishka

from bot.core import dto
from .inject import aiogram_middleware_inject
from bot.cache import UserCache
from bot.interactors.user import GetUserInteractor, CreateUserInteractor
from bot.core.enums import Languages


class RegisterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = structlog.get_logger(self.__class__.__name__)

    @aiogram_middleware_inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
        get_user: FromDishka[GetUserInteractor],
        create_user: FromDishka[CreateUserInteractor],
        cache: FromDishka[UserCache],
    ) -> Any:
        from_user: User | None = getattr(event, "from_user", None) or getattr(
            event, "event_from_user", None
        )
        if from_user is None:
            message: Message | None = getattr(event, "message", None)
            if message:
                from_user: User | None = getattr(message, "from_user", None)
        if from_user is None:
            return await handler(event, data)

        if not cache.settings.language:
            user = await get_user.execute(user_id=from_user.id)
            if user is None:
                user = await create_user.execute(
                    data=dto.CreateUserDTO(
                        user=dto.UserDTO(
                            telegram_id=from_user.id,
                            is_active=True,
                            is_admin=False,
                        ),
                        settings=dto.UserSettingsDTO(
                            language=Languages.RU
                            if from_user.language_code == Languages.RU
                            else Languages.EN,
                            user_id=from_user.id,
                        ),
                    )
                )
                await self.logger.info("Register new user", new_user=from_user.id)

            await self.update_cache(cache, user, from_user)

        return await handler(event, data)

    @staticmethod
    async def update_cache(
        cache: UserCache, db_user: dto.UserWithSettingsDTO, tg_user: User
    ):
        await cache.settings.id.set(str(db_user.settings.id))
        await cache.settings.language.set(
            Languages.RU if tg_user.language_code == Languages.RU else Languages.EN
        )
