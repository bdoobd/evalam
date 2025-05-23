from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# from pydantic import BaseModel

from app.dao.base import BaseDAO
from app.dao.session_maker import connection

from app.models.item import Item
from app.models.stock import Stock
from app.models.cat import Cat

from app.schemas.item import Item as ItemData, ItemWithID, FilterItems, ItemInStock
from app.schemas.stock import StockAdd


class ItemDAO(BaseDAO[Item]):
    model = Item

    @connection
    async def add_one(item_data: ItemData, session: AsyncSession) -> ItemData:
        new_item = await ItemDAO.add(session=session, values=item_data)

        return new_item

    @connection
    async def add_item_stock(stock_data: StockAdd, item_data: ItemData, session: AsyncSession) -> ItemData:
        stock = Stock(**stock_data.model_dump())
        session.add(stock)
        await session.flush()
        
        item = Item(**item_data.model_dump())
        item.stock_id = stock.id
        session.add(item)
        await session.commit()

        return item

    @connection
    async def get_items(filter: FilterItems, session: AsyncSession) -> ItemInStock:
        filter_dict = filter.model_dump(exclude_unset=True)
        query = (
            select(Item)
            .options(joinedload(Item.stock), joinedload(Item.cat))
            .filter_by(**filter_dict)
            .join(Stock)
            .join(Cat)
            .order_by(Stock.date.desc())
            .where(Stock.ready == False)
        )

        result = await session.execute(query)
        results = result.scalars().all()

        return [ItemInStock.model_validate(item) for item in results]

    # @connection
    # async def add_stock_and_item(
    #     cls, stock_data: dict, item_data: dict, session: AsyncSession
    # ):

    #     new_stock = Stock(**stock_data)

    #     session.add(new_stock)
    #     await session.flush()

    #     item = cls.model(**item_data, stock_id=new_stock.id)

    #     session.add(item)

    #     await session.commit()

    #     return new_stock.id

    # @connection
    # async def add_many_items(items_data: list[dict], session: AsyncSession):

    #     new_items = await ItemDAO.add_many(session=session, instances=items_data)

    #     print(f"New items added: {[item.id for item in new_items]}")

    #     return [item.id for item in new_items]

    # @connection
    # async def get_items(session: AsyncSession, filter: dict):

    #     items = await ItemDAO.find_all(session=session, **filter)

    #     return items

    # @connection
    # async def get_item_full_info(session: AsyncSession, item_id: int):

    #     item = await ItemDAO.get_item_info(session=session, id=item_id)

    #     return item

    # # ================================================================================
    # # ================================================================================
    @classmethod
    async def get_item_info(cls, session: AsyncSession, id: int):
        query = (
            select(cls.model)
            .options(joinedload(cls.model.stock))
            .options(joinedload(cls.model.cat))
            .where(cls.model.id == id)
        )

        result = await session.execute(query)
        records = result.unique().scalars().all()

        return records
