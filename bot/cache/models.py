from typing import Optional

from .base import DATA_TYPE, BaseModule, BaseUserCache
from .wrapper import FieldWrapper


class Settings(BaseModule):
    def __init__(self, parent: BaseUserCache) -> None:
        self._parent = parent
        self._data: DATA_TYPE = {}
        self.language = FieldWrapper(self, "language")
        self.id = FieldWrapper(self, "id")

    async def load(self) -> None:
        redis_key = self._make_redis_key()
        raw_data = await self._parent.redis.hgetall(redis_key)

        self._data = {
            k: int(v) if v.isdigit() else v for k, v in raw_data.items()
        }

    def _make_redis_key(self) -> str:
        return f"user:{self._parent.user_id}:settings"

    async def _save_field(self, field_name: str, value: Optional[str | int]) -> None:
        if value is None:
            value = ""
        redis_key = self._make_redis_key()
        await self._parent.redis.hset(redis_key, field_name, value)
        if self._parent.ex_time:
            await self._parent.redis.expire(redis_key, self._parent.ex_time)

    @property
    def data(self) -> DATA_TYPE:
        return self._data
