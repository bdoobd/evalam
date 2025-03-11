from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.cat import Cat
from app.dao.session_maker import connection
from app.schemas.cat import CatWithID


class CatDAO(BaseDAO[Cat]):
    model = Cat

    @connection
    async def add_one(cat_data: dict, session: AsyncSession) -> CatWithID:
        new_cat = await CatDAO.add(session=session, **cat_data)

        return new_cat.to_dict()

    @connection
    async def get_cats(session: AsyncSession) -> CatWithID:
        return await CatDAO.find_all(session=session)

    @connection
    async def get_cat_by_id(cat_id: int, session: AsyncSession) -> CatWithID:
        return await CatDAO.find_one_or_none(session=session, id=cat_id)

    @connection
    async def update_cat(
        cat_id: int, cat_data: dict, session: AsyncSession
    ) -> CatWithID:
        updated = await CatDAO.update(session=session, id=cat_id, values=cat_data)

        return updated

    @connection
    async def delete_cat_by_id(cat_id: int, session: AsyncSession):
        await CatDAO.delete_one_by_id(session=session, id=cat_id)
