from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.db_base import connection
from app.models.item import Item


class ItemDAO(BaseDAO):
    model = Item

    @connection
    async def add_one(item_data: dict, session: AsyncSession):

        new_item = await ItemDAO.add(session=session, **item_data)

        print(f"New item added: {new_item.id}")

        return new_item.id
