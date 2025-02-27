from abc import ABC, abstractmethod
from typing import Any


class AbstractSQLRepository(ABC):
    @abstractmethod
    async def get(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def destroy(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def list(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class AbstractNoSQLRepository(ABC):
    @abstractmethod
    async def set(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
