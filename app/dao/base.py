from typing import Any, Dict, List, Generic, TypeVar, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from pydantic import BaseModel

from app.dao.db_base import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):

        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
        else:
            filter_dict = {}

        try:
            query = select(cls.model).filter_by(**filter_dict)

            result = await session.execute(query)
            records = result.scalars().all()

            return records
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        try:
            query = select(cls.model).filter_by(**filter_dict)

            result = await session.execute(query)
            record = result.scalar_one_or_none()

            return record
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, id: int):
        try:
            return await session.get(cls.model, id)
        except SQLAlchemyError as e:
            print(f"Houston, we have error: {e}")
            raise

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[Dict[str, Any]]):
        new_instances = [cls.model(**instance) for instance in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return new_instances

    @classmethod
    async def update(cls, session: AsyncSession, id: int, values: BaseModel):
        found = await cls.find_one_or_none_by_id(session, id=id)

        if found is None:
            raise ValueError(f"{cls.model.__name__} with id {id} not found")

        for key, value in values.model_dump().items():
            setattr(found, key, value)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return found

    @classmethod
    async def delete_one_by_id(cls, session: AsyncSession, id: int):
        try:
            item = await session.get(cls.model, id)

            if item:
                await session.delete(item)
                await session.commit()

                return item
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
