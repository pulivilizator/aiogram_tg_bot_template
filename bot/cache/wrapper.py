from typing import Any, Optional

from .base import BaseModule


class FieldWrapper:
    """
    Обёртка над одним конкретным значением,
    позволяющая читать его как строку/число,
    и вызывать `await .set(...) / .del(...)` для обновления в Redis.
    """

    def __init__(
            self,
            parent: BaseModule,
            field_name: str,
            default: Optional[str | int] = None,
    ) -> None:
        """
        parent: ссылка на родителя (Settings, Profile, или сам UserCache),
                       откуда мы можем дотянуться до redis и user_id
        field_name: название поля (например, "language")
        default: значение по умолчанию, если ничего не нашлось
        """
        self._parent = parent
        self._field_name = field_name
        self._default = default

    def get_value(self) -> Optional[str| int]:
        return self._parent.data.get(self._field_name, self._default)

    async def set(self, value: str | int) -> None:
        self._parent.data[self._field_name] = value
        await self._parent._save_field(self._field_name, value)

    def __str__(self) -> str:
        val = self.get_value()
        return str(val) if val is not None else ""

    def __repr__(self) -> str:
        return repr(self.get_value())

    def __eq__(self, other: Any) -> bool:
        val = self.get_value()
        if isinstance(other, FieldWrapper):
            return val == other.get_value()
        return bool(val == other)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __bool__(self) -> bool:
        return bool(self.get_value())
