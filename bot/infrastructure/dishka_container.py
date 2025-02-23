def make_dishka_container():
    from bot.core.providers import get_providers
    from dishka import make_async_container
    return make_async_container(
        *get_providers()
    )