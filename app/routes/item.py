from fastapi import APIRouter, Depends

from app.schemas.item import ItemAdd
from app.dao.item import ItemDAO

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("/add_item", summary="Add item")
async def new_item(item: ItemAdd = Depends()) -> dict:

    item = await ItemDAO.add_one(item.model_dump())

    return {"message": "Item added", "result": item}
