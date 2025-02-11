from fastapi import APIRouter, Depends

from app.schemas.cat import CatAdd, CatWithID, Cat
from app.dao.cat import CatDAO

router = APIRouter(prefix="/cat", tags=["Тип продукта"])


@router.post("/new", summary="Добавить тип продукта")
async def new_cat(category: CatAdd = Depends()) -> dict:

    result = await CatDAO.add_one(category.model_dump(exclude_unset=True))

    return {"message": "Добавлена новая категория", "category": result}
