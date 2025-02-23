from dishka import Provider

from .cache import CacheProvider
from .common import CommonProvider
from .interactor import InteractorProvider
from .repository import RepositoryProvider


def get_providers() -> list[Provider]:
    return [
        CommonProvider(),
        CacheProvider(),
        RepositoryProvider(),
        InteractorProvider(),
    ]
