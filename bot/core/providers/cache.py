from aiogram.types import CallbackQuery, Message, TelegramObject, User
from dishka import Provider, Scope, from_context, provide
from redis.asyncio import Redis

from bot.cache import UserCache


class CacheProvider(Provider):
    event = from_context(provides=TelegramObject, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_user_cache(
        self,
        r: Redis,
        obj: TelegramObject,
    ) -> UserCache:
        from_user = getattr(obj, "from_user", None)
        if from_user is None:
            event = obj.event
            from_user: User = event.from_user
        return await UserCache(user_id=from_user.id, redis=r).load()
