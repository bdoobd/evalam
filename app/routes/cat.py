from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.cat import CatAdd, CatWithID, Cat
from app.schemas.user import User
from app.dao.cat import CatDAO
from app.dependencies import user_admin, user_powered

router = APIRouter(prefix="/cat", tags=["Тип продукта"])


@router.post("/new", summary="Добавить тип продукта")
async def new_cat(
    category: CatAdd, user: Annotated[User, Depends(user_powered)]
) -> CatWithID:

    result = await CatDAO.add_one(category.model_dump(exclude_unset=True))

    return result


@router.get("/cats", summary="Получить все категории продукта")
async def all_cats(user: Annotated[User, Depends(user_powered)]) -> list[CatWithID]:
    return await CatDAO.get_cats()


@router.get("/{cat_id}", summary="Получить категорию продукта по ID")
async def cat_by_id(
    cat_id: int, user: Annotated[User, Depends(user_powered)]
) -> CatWithID:

    print(cat_id)

    result = await CatDAO.get_cat_by_id(cat_id)

    return result
