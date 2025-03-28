from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.schemas.item import Item, ItemWithID, FilterItems, ItemAddWithNewStock
from app.dao.item import ItemDAO

# from app.schemas.stock import StockAdd
from app.schemas.user import User
from app.dependencies import user_powered, get_current_active_user

router = APIRouter(prefix="/item", tags=["Работа с товарами"])


@router.post("/new", summary="Добавление товара")
async def new_item(
    # item_data: Item | ItemAddWithNewStock, user: Annotated[User, Depends(user_powered)]
    item_data: ItemAddWithNewStock,
    user: Annotated[User, Depends(user_powered)],
):

    # item = await ItemDAO.add_one(item.model_dump(exclude_unset=True))

    print(item_data)

    return item_data


@router.get("/items", summary="Получение данных по продукту с фильтром")
# async def find_items(filter: Annotated[FilterItems, Query()]) -> list[ItemWithID]:
async def find_items(filter: Annotated[FilterItems, Query()]):

    return await ItemDAO.get_items(filter=filter.model_dump(exclude_none=True))


@router.get("/item/{item_id}", summary="Получение полной информации по товару")
async def get_item(item_id: int):

    item = await ItemDAO.get_item_full_info(item_id=item_id)

    return item


# @router.post("/new_many", summary="Add many items")
# async def new_many_item(items: list[ItemWithID]) -> dict:

#     # items = await ItemDAO.add_many([item.model_dump() for item in items])
#     items = [item.model_dump() for item in items]

#     result = await ItemDAO.add_many_items(items)

#     return {"message": "Items added", "result": result}


# @router.post("/add_stock_and_item", summary="Add stock and item")
# async def new_stock_and_item(stock: StockAdd, item: Item) -> dict:

#     item = await ItemDAO.add_stock_and_item(stock.model_dump(), item.model_dump())

#     return {"message": "Item and stock added", "Added ID": item}
