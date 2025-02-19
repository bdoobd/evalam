from fastapi import APIRouter, Depends

from app.schemas.item import Item, ItemWithID
from app.dao.item import ItemDAO
from app.schemas.stock import StockAdd

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("/new", summary="Добавление товара")
async def new_item(item: Item) -> ItemWithID:

    item = await ItemDAO.add_one(item.model_dump(exclude_unset=True))

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
