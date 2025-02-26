from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.cat import CatAdd, CatWithID, Cat
from app.schemas.user import User
from app.dao.cat import CatDAO
from app.dependencies import user_admin, user_powered

router = APIRouter(prefix="/cat", tags=["Тип продукта"])


@router.post("/new", summary="Добавить тип продукта")
# async def new_cat(category: CatAdd = Depends()) -> CatWithID:
async def new_cat(category: CatAdd):
    # async def new_cat(
    #     category: CatAdd, user: Annotated[User, Depends(user_powered)]
    # ) -> CatWithID:
    print(category)

    return {"data": category}

    # result = await CatDAO.add_one(category.model_dump(exclude_unset=True))

    # return result


@router.get("/cats", summary="Получить все категории продукта")
async def all_cats(user: Annotated[User, Depends(user_powered)]) -> list[CatWithID]:
    return await CatDAO.get_cats()
