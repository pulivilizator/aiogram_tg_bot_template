from dishka import Provider

from .cache_provider import CacheProvider
from .common_provider import CommonProvider

def get_providers() -> list[Provider]:
    return [
        CommonProvider(),
        CacheProvider(),
    ]