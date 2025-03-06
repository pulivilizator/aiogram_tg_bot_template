from typing import Protocol, runtime_checkable

from aiogram.types import User


@runtime_checkable
class HasFromUser(Protocol):
    from_user: User


@runtime_checkable
class HasEventFromUser(Protocol):
    event_from_user: User


@runtime_checkable
class HasEvent(Protocol):
    event: HasFromUser


class WidgetEnum(Protocol):
    @property
    def WIDGET_KEY(self) -> str:  # noqa #N802
        pass
