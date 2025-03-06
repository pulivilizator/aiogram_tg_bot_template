from typing import runtime_checkable, Protocol, ReadOnly, Final

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
    def WIDGET_KEY(self) -> str:
        pass