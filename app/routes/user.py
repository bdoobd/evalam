from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_user
from app.dependencies import fake_users, fake_hash_password
from app.schemas.user import User, UserInDB

router = APIRouter(prefix="/user", tags=["Создание полльзователей"])


@router.get("/users/me", summary="Display user information")
async def read_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/token", summary="Auth token endpoint")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users.get(form_data.username)

    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    user = UserInDB(**user_dict)

    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashedpwd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {"access_token": user.username, "token_type": "bearer"}
