from typing import Annotated
from sqlalchemy import Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    class_mapper,
)
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from app.config import settings

DB_URL = settings.get_db_url()
engine = create_async_engine(url=DB_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

str_req = Annotated[str, mapped_column(nullable=False)]
str_req_uq = Annotated[str, mapped_column(nullable=False, unique=True)]
str_opt = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def to_dict(self) -> dict:
        columns = class_mapper(self.__class__).columns

        return {column.key: getattr(self, column.key) for column in columns}


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, **kwargs, session=session)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
