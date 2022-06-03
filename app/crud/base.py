from typing import (
    Generic, List, Optional, Type, TypeVar, Union, Collection
)

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        self.model = model

    async def get(
            self,
            pk: int, session: AsyncSession
    ) -> Optional[ModelType]:
        result = await session.execute(
            select(self.model).where(self.model.id == pk)
        )
        return result.scalars().first()

    async def get_multi(self, session: AsyncSession) -> List[ModelType]:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(
            self, data: CreateSchemaType, session: AsyncSession,
            **attributes,
    ) -> ModelType:
        obj = self.model(
            **{**data.dict(), **attributes}
        )
        await self.save(obj, session)
        return obj

    async def update(
            self,
            obj: ModelType, data: UpdateSchemaType,
            session: AsyncSession,
            **attributes,
    ) -> ModelType:
        data = {**data.dict(exclude_unset=True), **attributes}
        [setattr(obj, field, data[field]) for field in jsonable_encoder(obj)
         if field in data]
        await self.save(obj, session)
        return obj

    async def remove(
            self,
            obj: ModelType,
            session: AsyncSession
    ) -> ModelType:
        await session.delete(obj)
        await session.commit()
        return obj

    async def get_by_attribute(
            self,
            attr_name: str, attr_value: str,
            session: AsyncSession,
            order_by: str = None,
            many=False,
            desc=False
    ) -> Union[List[ModelType], Optional[ModelType]]:
        attr = getattr(self.model, attr_name)
        select_stmt = select(self.model).where(attr == attr_value)
        if order_by is not None:
            order_attr = getattr(self.model, order_by)
            if desc:
                select_stmt = select_stmt.order_by(order_attr.desc())
            else:
                select_stmt = select_stmt.order_by(order_attr)
        result = await session.execute(select_stmt)
        if many:
            return result.scalars().all()
        return result.scalars().first()

    async def save(
            self, obj: Union[ModelType, Collection[ModelType]],
            session: AsyncSession,
            many=False
    ) -> None:
        session.add_all(obj) if many else session.add(obj)
        await session.commit()
        if many:
            [await session.refresh(single_obj) for single_obj in obj]
        else:
            await session.refresh(obj)
