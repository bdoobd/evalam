from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.stock import Stock
from app.db_base import connection


class StockDAO(BaseDAO):
    model = Stock

    @connection
    async def add_one(stock_data: dict, session: AsyncSession):

        # stock_data["date_in"] = datetime.strptime(stock_data["date_in"], "%Y-%m-%d")

        new_stock = await StockDAO.add(session=session, **stock_data)

        print(f"New stock added: {new_stock.id}")

        return new_stock.id
