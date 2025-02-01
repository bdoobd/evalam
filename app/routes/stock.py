from fastapi import APIRouter, Depends

from app.dao.stock import StockDAO
from app.schemas.stock import StockAdd, Stock, StockRef, StockData

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.post("/add_stock", summary="Add stock")
async def new_stock(stock: StockAdd = Depends()) -> dict:
    stock = await StockDAO.add_one(stock.model_dump())

    return {"message": "Stock added", "Stock ID": stock}


@router.get("/get_all", summary="Get all stock")
async def get_all_stock():
    stocks = await StockDAO.get_all_stocks()

    print(stocks)

    return stocks


@router.get("/get_refs", summary="Get all stock references")
async def get_all_stock_refs() -> list[StockRef]:
    refs = await StockDAO.stock_refs()

    return refs


@router.get("/get_stock/{stock_id}", summary="Get stock by ID")
async def get_stock_by_id(stock_id: int):
    stock = await StockDAO.fetch_stock_by_id(stock_id)

    # print(type(stock))

    return stock


@router.get("/get_stock_with_items", summary="Get stock with item")
async def get_full_stock() -> list[StockData]:
    stocks = await StockDAO.get_stock_and_items()

    return stocks
