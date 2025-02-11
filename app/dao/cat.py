from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.cat import Cat
from app.db_base import connection
from app.schemas.cat import CatWithID


class CatDAO(BaseDAO):
    model = Cat

    @connection
    async def add_one(cat_data: dict, session: AsyncSession) -> CatWithID:
        new_cat = await CatDAO.add(session=session, **cat_data)

        return new_cat.to_dict()
