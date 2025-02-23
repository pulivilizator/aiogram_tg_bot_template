from aiogram.types import TelegramObject, User

from dishka import Provider, provide, Scope, from_context
from redis.asyncio import Redis

from bot.cache import UserCache


class CacheProvider(Provider):
    event = from_context(provides=TelegramObject, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_user_cache(self, r: Redis, obj: TelegramObject) -> UserCache:
        from_user = getattr(obj, "from_user", None)
        if from_user is None:
            event = getattr(obj, "event")
            from_user: User = getattr(event, "from_user")
        return await UserCache(user_id=from_user.id, redis=r).load()
