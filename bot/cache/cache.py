import asyncio
from typing import Self, Optional

from redis.asyncio import Redis

from .models import Settings
from ..core.enums import CacheLoadModules


class UserCache:
    def __init__(self, user_id: int, redis: Redis) -> None:
        self.user_id = user_id
        self.redis = redis
        self.settings = Settings(self)

    async def load(self, load_modules: Optional[list[CacheLoadModules]] = None) -> Self:
        if load_modules is None:
            load_modules = list(CacheLoadModules)
        tasks = [getattr(self, module).load() for module in load_modules]
        await asyncio.gather(*tasks)
        return self
