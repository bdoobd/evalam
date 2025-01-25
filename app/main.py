from datetime import datetime
from fastapi import FastAPI

from app.db_base import connection
from app.models.stock import Stock
from app.dao.stock import StockDAO

from app.routes.stock import router as stock_router

app = FastAPI()


@app.get("/", summary="Root endpoint")
async def index():
    return {"message": "Root of service"}


app.include_router(stock_router)


# @app.post("/add_stock", summary="Add stock")
# async def new_stock(stock: dict):

#     await StockDAO.add_one(stock)

#     return {"message": "Stock added"}


# @app.post("/add_stocks", summary="Add multiply stocks")
# async def new_stocks(stocks: list[dict]):

#     stocks = map(
#         lambda stock: {
#             **stock,
#             "date_in": datetime.strptime(stock["date_in"], "%Y-%m-%d"),
#         },
#         stocks,
#     )

#     res = await add_stocks(stocks)

#     return {"message": "Stocks added", "result": res}


# =================================


@connection
async def add_stocks(
    stocks: list[dict],
    session,
):

    stock_list = [
        Stock(
            reference=stock["reference"],
            date_in=stock["date_in"],
            sender=stock["sender"],
            note=stock["note"],
        )
        for stock in stocks
    ]

    session.add_all(stock_list)

    await session.commit()

    return [stock.id for stock in stock_list]
