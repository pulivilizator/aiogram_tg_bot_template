from aiogram.types import TelegramObject
from dishka import Provider, Scope, from_context, provide
from redis.asyncio import Redis

from bot.cache import UserCache
from bot.core.protocols import HasEvent, HasFromUser


class CacheProvider(Provider):
    event = from_context(provides=TelegramObject, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_user_cache(
        self,
        r: Redis,  # type: ignore
        obj: TelegramObject,
    ) -> UserCache:
        if isinstance(obj, HasFromUser):
            from_user = obj.from_user
        elif isinstance(obj, HasEvent):
            from_user = obj.event.from_user
        else:
            raise ValueError(f"Unable to define from_user for an object of type {type(obj).__name__}")
        if from_user is None:
            raise ValueError("The from_user attribute is missing")
        return await UserCache(user_id=from_user.id, redis=r).load()
