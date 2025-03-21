from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from pydantic import create_model

from app.dao.base import BaseDAO
from app.models.stock import Stock
from app.models.item import Item
from app.dao.session_maker import connection
from app.schemas.stock import StockData, StockWithID, StockAdd
from app.schemas.item import ItemWithID


class StockDAO(BaseDAO[Stock]):
    model = Stock

    @connection
    async def get_on_stock(session: AsyncSession) -> list[StockWithID]:
        OnStock = create_model("OnStock", ready=(bool, ...))
        return await StockDAO.find_all(session=session, filters=OnStock(ready=False))

    @connection
    async def get_all_stocks(session: AsyncSession):
        result = await StockDAO.find_all(session=session)

        return result

    @connection
    async def find_stock_by_id(stock_id: int, session: AsyncSession) -> StockWithID:
        # result = await StockDAO.find_one_or_none_by_id(session=session, id=stock_id)
        StockId = create_model("StockId", id=(int, ...))
        try:
            return await StockDAO.find_one_or_none(
                session=session, filters=StockId(id=stock_id)
            )
        except SQLAlchemyError as e:
            return {"message": "Stock not found"}

    @connection
    async def add_one(stock_data: StockAdd, session: AsyncSession) -> StockWithID:

        new_stock = await StockDAO.add(session=session, values=stock_data)

        return new_stock

    @connection
    async def update_stock(
        stock_id: int, stock: StockWithID, session: AsyncSession
    ) -> StockWithID:
        return await StockDAO.update(session=session, id=stock_id, values=stock)

    @connection
    async def delete_stock(stock_id: int, session: AsyncSession) -> StockWithID:
        return await StockDAO.delete_one_by_id(session=session, id=stock_id)

    # @connection
    # async def get_stock_and_items(session: AsyncSession):
    #     result = await StockDAO.get_stock_with_item(session=session)
    #     # NOTE: Из за вложенного SQLAlchemy объекта в item_data не удаётся конвертировать в модель Pydantic автоматически, поэтому мануальная конвертация
    #     stock_list = [
    #         StockData(
    #             id=stock.id,
    #             reference=stock.reference,
    #             date_in=stock.date_in,
    #             sender=stock.sender,
    #             note=stock.note,
    #             item_data=(
    #                 [
    #                     ItemAddWithID.model_validate(item.to_dict())
    #                     for item in stock.items
    #                 ]
    #                 if stock.items
    #                 else []
    #             ),
    #         )
    #         for stock in result
    #     ]

    #     return stock_list

    # @connection
    # async def stock_refs(session: AsyncSession):
    #     result = await StockDAO.get_refs_with_id(session=session)

    #     return result
    # ================================================
    # ================================================
    # @classmethod
    # async def get_refs_with_id(cls, session: AsyncSession):
    #     query = select(cls.model.id, cls.model.reference)
    #     result = await session.execute(query)
    #     records = result.all()

    #     return records
