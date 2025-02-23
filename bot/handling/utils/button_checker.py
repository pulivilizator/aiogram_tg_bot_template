import asyncio
from enum import StrEnum
from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedWidget
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.cache import UserCache


class SetButtonChecked:
    def __init__(self, *keys: StrEnum):
        self._keys = keys

    @inject
    async def __call__(self, _: Any, dialog_manager: DialogManager, cache: FromDishka[UserCache]):
        await self._set_default_buttons(_, dialog_manager=dialog_manager, keys=self._keys, cache=cache)

    async def _set_checked(self, cache: UserCache, dialog_manager: DialogManager, key):
        user_value = str(cache.find(key.WIDGET_KEY))
        widget: ManagedWidget = dialog_manager.find(key.WIDGET_KEY)
        await widget.set_checked(user_value)

    async def _set_default_buttons(self, _, dialog_manager: DialogManager, keys, cache: UserCache):
        await asyncio.gather(
            *[
                asyncio.create_task(self._set_checked(cache, dialog_manager, cache_key))
                for cache_key in keys
            ]
        )
