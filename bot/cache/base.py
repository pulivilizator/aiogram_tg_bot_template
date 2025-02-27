from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self, TypeAlias

from redis.asyncio import Redis

from bot.core.enums import CacheLoadModules

DATA_TYPE: TypeAlias = dict[str, str | int]

class BaseCache(ABC):
    redis: Redis[str]
    ex_time: int | None

    @abstractmethod
    async def load(self, load_modules: list[CacheLoadModules] | None = None) -> Self:
        raise NotImplementedError

    @abstractmethod
    def find(self, key: str) -> str | int | None:
        raise NotImplementedError

class BaseUserCache(BaseCache, ABC):
    user_id: int | str

class BaseModule(ABC):
    _data: DATA_TYPE

    @abstractmethod
    async def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _make_redis_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def _save_field(self, field_name: str, value: str | int | None) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self) -> DATA_TYPE:
        return self._data