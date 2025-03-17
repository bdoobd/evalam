from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.cat import Cat
from app.dao.session_maker import connection
from app.schemas.cat import CatWithID, CatAdd, CatByID


class CatDAO(BaseDAO[Cat]):
    model = Cat

    @connection
    async def add_category(cat_data: CatAdd, session: AsyncSession) -> CatWithID:
        new_cat = await CatDAO.add(session=session, values=cat_data)

        return new_cat.to_dict()

    @connection
    async def get_cats(session: AsyncSession) -> list[CatWithID]:
        return await CatDAO.find_all(session=session)

    @connection
    async def get_cat_by_id(cat_id: int, session: AsyncSession) -> CatWithID:
        return await CatDAO.find_one_or_none(
            session=session, filters=CatByID(id=cat_id)
        )

    @connection
    async def update_cat(
        cat_id: int, cat_data: CatAdd, session: AsyncSession
    ) -> CatWithID:

        updated = await CatDAO.update(session=session, id=cat_id, values=cat_data)

        return updated

    @connection
    async def delete_cat_by_id(cat_id: int, session: AsyncSession):
        await CatDAO.delete_one_by_id(session=session, id=cat_id)
