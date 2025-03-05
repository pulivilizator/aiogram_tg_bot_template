from typing import runtime_checkable, Protocol

from aiogram.types import User


@runtime_checkable
class HasFromUser(Protocol):
    from_user: User

@runtime_checkable
class HasEvent(Protocol):
    event: HasFromUser