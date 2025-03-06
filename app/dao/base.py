from typing import Any, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from pydantic import BaseModel


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, session: AsyncSession, **kwargs):
        new_instance = cls.model(**kwargs)
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
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)

        result = await session.execute(query)
        records = result.scalars().all()

        return records

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)

        result = await session.execute(query)
        record = result.scalar_one_or_none()

        return record

    @classmethod
    async def update(cls, session: AsyncSession, id: int, values: BaseModel):
        found = await cls.find_one_or_none(session, id=id)
        if found is None:
            raise ValueError(f"{cls.model.__name__} with id {id} not found")

        for key, value in values.items():
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
            cat = await session.get(cls.model, id)

            if cat:
                await session.delete(cat)
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
