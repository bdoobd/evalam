from typing import Annotated

from fastapi import APIRouter, Depends

from app.dao.stock import StockDAO
from app.dependencies import get_current_active_user, user_powered
from app.schemas.stock import StockAdd, StockWithID, Stock
from app.schemas.user import User

router = APIRouter(prefix="/stock", tags=["Записи склада"])


@router.get("/stocks", summary="Получить все записи склада")
async def get_all_stock(
    user: Annotated[User, Depends(get_current_active_user)],
) -> list[StockWithID]:

    stocks = await StockDAO.get_all_stocks()

    return stocks


@router.get("/onstock", summary="Получить все референсы на складе")
async def get_on_stock(
    user: Annotated[User, Depends(get_current_active_user)],
) -> list[StockWithID]:

    return await StockDAO.get_on_stock()


@router.get("/{stock_id}", summary="Получить запись склада по ID")
async def get_stock_by_id(
    stock_id: int, user: Annotated[User, Depends(get_current_active_user)]
) -> StockWithID:
    stock = await StockDAO.find_stock_by_id(stock_id)

    return stock


@router.post("/new", summary="Добавление склаского номреа")
async def new_stock(
    stock: StockAdd, user: Annotated[User, Depends(user_powered)]
) -> StockWithID:

    return await StockDAO.add_one(stock)


@router.put("/{stock_id}", summary="Обновить запись склада")
async def update_stock(
    stock_id: int, stock: StockWithID, user: Annotated[User, Depends(user_powered)]
) -> StockWithID:

    return await StockDAO.update_stock(stock_id, stock)


@router.delete("/{id}", summary="Удалить запись склада")
async def delete_stock(
    id: int, user: Annotated[User, Depends(user_powered)]
) -> StockWithID:

    return await StockDAO.delete_stock(id)


# @router.delete("/{stock_id}", summary="Удалить запись склада")
# async def delete_stock(
#     stock_id: int, user: Annotated[User, Depends(user_powered)]
# ) -> StockWithID:

#     return await StockDAO.delete_stock(stock_id)


# @router.get("/get_stock_with_items", summary="Get stock with item")
# async def get_full_stock() -> list[StockData]:
#     stocks = await StockDAO.get_stock_and_items()

#     return stocks
