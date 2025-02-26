from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject, User
from dishka.integrations.aiogram import FromDishka
from fluentogram import TranslatorHub

from bot.cache import UserCache
from bot.core import dto
from bot.core.enums import Languages
from bot.interactors.user import UpdateUserSettingsInteractor

from .inject import aiogram_middleware_inject


class TranslatorRunnerMiddleware(BaseMiddleware):
    @aiogram_middleware_inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
        hub: FromDishka[TranslatorHub],
        cache: FromDishka[UserCache],
        user_settings_update: FromDishka[UpdateUserSettingsInteractor],
    ) -> Any:
        cb: CallbackQuery | None = getattr(event, "callback_query", None)
        from_user: User | None = getattr(cb, "from_user", None)

        lang = await self._get_lang(cb, from_user, cache, user_settings_update)
        data["i18n"] = hub.get_translator_by_locale(lang)
        return await handler(event, data)

    @staticmethod
    async def _get_lang(
        cb: CallbackQuery,
        user: User,
        cache: UserCache,
        update_settings: UpdateUserSettingsInteractor,
    ) -> str:
        if cb and Languages.WIDGET_KEY in cb.data:
            lang = (
                Languages.RU if cb.data.split(":")[1] == Languages.RU else Languages.EN
            )
            await cache.settings.language.set(lang)
            await update_settings.execute(
                settings_id=str(cache.settings.id),
                data=dto.UpdateUserSettingsDTO(language=lang),
            )
            return lang
        return str(cache.settings.language)
