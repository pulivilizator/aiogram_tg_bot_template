from abc import ABC, abstractmethod

from .wrapper import FieldWrapper


class BaseModule(ABC):
    @abstractmethod
    async def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _make_redis_key(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _save_field(self, field_name: str, value) -> None:
        raise NotImplementedError


class Settings(BaseModule):
    def __init__(self, parent):
        self._parent = parent
        self._data = {}
        self.language = FieldWrapper(self, "language")
        self.id = FieldWrapper(self, "id")

    async def load(self):
        redis_key = self._make_redis_key()
        raw_data = await self._parent.redis.hgetall(redis_key)
        self._data = {k.decode(): v.decode() for k, v in raw_data.items()}

    def _make_redis_key(self) -> str:
        return f"user:{self._parent.user_id}:settings"

    async def _save_field(self, field_name: str, value):
        redis_key = self._make_redis_key()
        await self._parent.redis.hset(redis_key, field_name, value)
        await self._parent.redis.expire(redis_key, self._parent.ex_time)
