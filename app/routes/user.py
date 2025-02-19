from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from app.dao.user import UserDAO
from app.schemas.user import UserRegister, UserData, User
from app.schemas.token import Token
from app.auth.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.config import get_auth_token_data
from app.dependencies import user_admin, get_current_active_user

router = APIRouter(prefix="/user", tags=["Работа с пользователями"])


@router.post("/login", summary="Логин пользователя")
async def login(
    response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:

    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
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
    user_data: Annotated[UserRegister, Depends()],
    user: Annotated[User, Depends(user_admin)],
) -> UserData:
    user_exists = await UserDAO.find_user({"username": user_data.username})

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )

    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = get_password_hash(user_data.password)
    user = await UserDAO.add_user(user_dict)

    return user


@router.get("/me", summary="Получение информации о текущем пользователе")
async def get_me(user: Annotated[User, Depends(get_current_active_user)]) -> UserData:
    return user
