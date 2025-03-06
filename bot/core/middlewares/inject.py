from typing import Callable, ParamSpec, TypeVar

from dishka.integrations.base import wrap_injection

T = TypeVar("T")
P = ParamSpec("P")


def aiogram_middleware_inject(func: Callable[P, T]) -> Callable[P, T]:
    return wrap_injection(
        func=func,
        is_async=True,
        container_getter=lambda args, kwargs: args[3]["dishka_container"],
    )
