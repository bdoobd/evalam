from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.dao.user import UserDAO
from app.schemas.user import UserRegister, UserData, User, UserLogin
from app.schemas.token import Token
from app.auth.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.config import get_auth_token_data
from app.dependencies import user_admin, get_current_active_user
from app.exceptions import IncorrectPasswordException
from app.helpers.roles import Roles


router = APIRouter(prefix="/user", tags=["Работа с пользователями"])


@router.post("/login", summary="Логин пользователя")
async def login(response: Response, form_data: UserLogin) -> Token:

    user = await authenticate_user(form_data.username, form_data.password)
    breakpoint()
    if not user:
        raise IncorrectPasswordException()

    auth_data = get_auth_token_data()
    access_token_expires = timedelta(minutes=auth_data["expire"])
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response.set_cookie(key="pass_token", value=access_token, httponly=True)

    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout", summary="Выход из системы")
async def logout(response: Response):
    response.delete_cookie(key="pass_token")
    return {"message": "Выход выполнен"}


@router.post("/register", summary="Регистрация нового пользователя")
async def register(
    user_data: UserRegister,
    user: Annotated[User, Depends(user_admin)],
) -> UserData:

    user_exists = await UserDAO.find_user({"username": user_data.username})

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )

    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пароль и подтверждение не совпадают",
        )

    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = get_password_hash(user_data.password)
    user_dict.pop("confirm_password")
    user = await UserDAO.add_user(user_dict)

    return user


@router.get("/me", summary="Получение информации о текущем пользователе")
async def get_me(user: Annotated[User, Depends(get_current_active_user)]) -> UserData:
    return user


@router.get("/all", summary="Получить всех пользователей")
async def all_users(user: Annotated[User, Depends(user_admin)]) -> list[UserData]:
    return await UserDAO.find_all_users()


@router.get("/roles", summary="Получить все роли для пользователя")
async def get_roles() -> dict:
    roles = {role: role.title() for role in Roles}

    return roles


@router.get("/{user_id}", summary="Получить данные пользователя по ID")
async def get_user(
    user_id: int, user: Annotated[User, Depends(user_admin)]
) -> UserData:
    return await UserDAO.find_user({"id": user_id})


@router.delete("/{user_id}", summary="Удалить пользователя по ID")
async def delete_user(user_id: int, user: Annotated[User, Depends(user_admin)]) -> dict:
    await UserDAO.delete_user_by_id(user_id=user_id)

    return {"message": "User delete successfully"}
