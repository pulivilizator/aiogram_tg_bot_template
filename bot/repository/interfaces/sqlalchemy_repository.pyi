# sqlalchemy_repository.pyi

from logging import Logger
from typing import Any, Generic, Optional, overload, Type
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Query
from structlog import get_logger
from typing_extensions import TypeVar

from bot.repository.interfaces.base import AbstractSQLRepository

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
DTOModel = TypeVar("DTOModel", bound=BaseModel)
DTOModelResponse = TypeVar("DTOModelResponse", bound=BaseModel)

class SQLAlchemyRepository(Generic[ModelType, DTOModel], AbstractSQLRepository):
    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType],
        dto_model: type[DTOModel],
        lookup_field: str,
    ) -> None:
        self._session = session
        self._model = model
        self._lookup_field = lookup_field
        self._dto_model = dto_model
        self.logger = get_logger(__name__).bind(
            repository=self.__class__.__name__,
            model=self._model.__name__,
        )

    async def get_instance(self, lookup_value: Any) -> ModelType:
        ...

    # ------------------------------------------------
    # get
    # ------------------------------------------------
    @overload
    async def get(self, lookup_value: Any, response_model: None = ...) -> DTOModel:
        ...
    @overload
    async def get(self, lookup_value: Any, response_model: Type[DTOModelResponse]) -> DTOModelResponse:
        ...

    # ------------------------------------------------
    # get_or_none
    # ------------------------------------------------
    @overload
    async def get_or_none(
        self,
        lookup_value: Any,
        response_model: None = ...,
    ) -> DTOModel | None:
        ...
    @overload
    async def get_or_none(
        self,
        lookup_value: Any,
        response_model: Type[DTOModelResponse],
    ) -> DTOModelResponse | None:
        ...
    # ------------------------------------------------
    # create
    # ------------------------------------------------
    @overload
    async def create(
        self,
        model_data: BaseModel,
        response_model: None = ...,
    ) -> DTOModel:
        ...
    @overload
    async def create(
        self,
        model_data: BaseModel,
        response_model: Type[DTOModelResponse],
    ) -> DTOModelResponse:
        ...

    # ------------------------------------------------
    # get_or_create
    # ------------------------------------------------
    @overload
    async def get_or_create(
        self,
        lookup_value: Any,
        model_data: BaseModel,
        response_model: None = ...,
    ) -> DTOModel:
        ...
    @overload
    async def get_or_create(
        self,
        lookup_value: Any,
        model_data: BaseModel,
        response_model: Type[DTOModelResponse],
    ) -> DTOModelResponse:
        ...

    # ------------------------------------------------
    # update
    # ------------------------------------------------
    @overload
    async def update(
        self,
        lookup_value: Any,
        update_data: BaseModel,
        response_model: None = ...,
    ) -> DTOModel:
        ...
    @overload
    async def update(
        self,
        lookup_value: Any,
        update_data: BaseModel,
        response_model: Type[DTOModelResponse],
    ) -> DTOModelResponse:
        ...

    # ------------------------------------------------
    # destroy
    # ------------------------------------------------
    async def destroy(self, lookup_value: Any) -> None:
        ...

    # ------------------------------------------------
    # list
    # ------------------------------------------------
    @overload
    async def list(
        self,
        filter_query: None = ...,
        response_model: None = ...,
    ) -> list[DTOModel]:
        ...
    @overload
    async def list(
        self,
        filter_query: Query[Any],
        response_model: None,
    ) -> list[DTOModel]:
        ...
    @overload
    async def list(
        self,
        filter_query: None,
        response_model: Type[DTOModelResponse],
    ) -> list[DTOModelResponse]:
        ...
    @overload
    async def list(
        self,
        filter_query: Query[Any],
        response_model: Type[DTOModelResponse],
    ) -> list[DTOModelResponse]:
        ...
