from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_user, get_current_active_user
from app.schemas.user import User, UserInDB
from app.schemas.token import Token
from app.auth.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    fake_users,
)
from app.config import get_auth_token_data

router = APIRouter(prefix="/user", tags=["Создание полльзователей"])


@router.get("/users/me", summary="Display user information")
async def read_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.post("/token", summary="Auth token endpoint")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(fake_users, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=get_auth_token_data()["expire"])
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/hashed_pwd", summary="TEST")
async def get_hash(password: str) -> str:
    return get_password_hash(password)
