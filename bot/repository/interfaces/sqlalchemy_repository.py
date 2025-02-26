from typing import Any, Generic, Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
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
    ):
        self._session = session
        self._model = model
        self._lookup_field = lookup_field
        self._dto_model = dto_model
        self.logger = get_logger(__name__).bind(
            repository=self.__class__.__name__,
            model=self._model.__name__,
        )

    async def get_instance(self, lookup_value: Any) -> ModelType:
        lookup_field = getattr(self._model, self._lookup_field)
        if lookup_field is None:
            raise ValueError("Model does not have a lookup field")
        query = select(self._model).where(lookup_field == lookup_value)
        result = await self._session.execute(query)
        instance: ModelType | None = result.scalars().first()
        if instance is None:
            await self.logger.warning(
                f"Instance with {lookup_field} == {lookup_value} not found",
            )
            raise NoResultFound(
                f"Instance with {lookup_field} == {lookup_value} not found",
            )
        return instance

    async def get(
        self,
        lookup_value: Any,
        response_model: Optional[type[DTOModelResponse]] = None,
    ) -> DTOModel | DTOModelResponse:
        instance = await self.get_instance(lookup_value)
        if response_model is None:
            return self._dto_model.model_validate(instance, from_attributes=True)
        return response_model.model_validate(instance, from_attributes=True)

    async def get_or_none(
        self,
        lookup_value: Any,
        response_model: Optional[type[DTOModelResponse]] = None,
    ) -> DTOModel | DTOModelResponse | None:
        try:
            instance = await self.get_instance(lookup_value)
        except NoResultFound:
            return None

        if response_model is None:
            return self._dto_model.model_validate(instance, from_attributes=True)
        return response_model.model_validate(instance, from_attributes=True)

    async def create(
        self,
        model_data: BaseModel,
        response_model: Optional[type[DTOModelResponse]] = None,
    ) -> DTOModel | DTOModelResponse:
        new_model = self._model(**model_data.model_dump(exclude_unset=True))
        self._session.add(new_model)
        await self.logger.info(f"Model {model_data} created")
        if response_model is None:
            return self._dto_model.model_validate(new_model, from_attributes=True)
        return response_model.model_validate(new_model, from_attributes=True)

    async def get_or_create(
        self,
        lookup_value: Any,
        model_data: BaseModel,
        response_model: Optional[type[DTOModelResponse]] = None,
    ) -> DTOModel | DTOModelResponse:
        obj = await self.get_or_none(lookup_value, response_model)
        if obj is None:
            return await self.create(model_data, response_model)
        return obj

    async def update(
        self,
        lookup_value,
        update_data: BaseModel,
        response_model: Optional[type[DTOModelResponse]] = None,
    ) -> DTOModel | DTOModelResponse:
        obj = await self.get_instance(lookup_value)
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
            else:
                await self.logger.error(f"Model does not have attribute {key}")
                raise AttributeError(f"Model does not have attribute {key}")
        await self._session.commit()
        await self._session.refresh(obj)
        if response_model is None:
            return self._dto_model.model_validate(obj, from_attributes=True)
        return response_model.model_validate(obj, from_attributes=True)

    async def destroy(self, lookup_value) -> None:
        obj = await self.get_instance(lookup_value)
        await self._session.delete(obj)
        await self._session.commit()
        await self.logger.info(f"Model {obj} destroyed")

    async def list(
        self,
        filter_query: Optional[Query] = None,
        response_model: Optional[type[DTOModelResponse]] = None,
    ) -> list[DTOModel | DTOModelResponse]:
        if filter_query is None:
            result = await self._session.execute(select(self._model))
        else:
            result = await self._session.execute(filter_query)
        resp_model = self._dto_model if response_model is None else response_model
        return [
            resp_model.model_validate(obj, from_attributes=True)
            for obj in result.scalars().all()
        ]
