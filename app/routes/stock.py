from typing import Annotated

from fastapi import APIRouter, Depends

from app.dao.stock import StockDAO
from app.dependencies import get_current_active_user, user_powered
from app.schemas.stock import StockAdd, StockWithID, StockData
from app.schemas.user import User

router = APIRouter(prefix="/stock", tags=["Записи слада"])


@router.post("/new", summary="Добавление склаского номреа")
async def new_stock(
    stock: StockAdd, user: Annotated[User, Depends(user_powered)]
) -> StockWithID:
    result = await StockDAO.add_one(stock.model_dump(exclude_unset=True))

    return result


@router.get("/stocks", summary="Get all stock")
async def get_all_stock(
    user: Annotated[User, Depends(get_current_active_user)]
) -> list[StockWithID]:
    stocks = await StockDAO.get_all_stocks()

    return stocks


# @router.get("/get_refs", summary="Get all stock references")
# async def get_all_stock_refs() -> list[StockWithID]:
#     refs = await StockDAO.stock_refs()

#     return refs


# @router.get("/get_stock/{stock_id}", summary="Get stock by ID")
# async def get_stock_by_id(stock_id: int):
#     stock = await StockDAO.fetch_stock_by_id(stock_id)

#     # print(type(stock))

#     return stock


# @router.get("/get_stock_with_items", summary="Get stock with item")
# async def get_full_stock() -> list[StockData]:
#     stocks = await StockDAO.get_stock_and_items()

#     return stocks
