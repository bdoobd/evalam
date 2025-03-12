from typing import Annotated

from fastapi import Depends, HTTPException, status, Request
from jwt.exceptions import InvalidTokenError

from app.schemas.user import UserData
from app.auth.auth import decode_access_token
from app.schemas.token import TokenData
from app.dao.user import UserDAO
from app.exceptions import InvalidTokenException, TokenNotFoundException


def get_token(request: Request):
    token = request.cookies.get("pass_token")

    if not token:
        raise TokenNotFoundException

    return token


async def get_current_user(token: Annotated[str, Depends(get_token)]) -> UserData:

    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")

        if username is None:
            raise InvalidTokenException

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise InvalidTokenException

    # user = await UserDAO.find_user({"username": token_data.username})
    user = await UserDAO.find_user(token_data)

    if user is None:
        raise InvalidTokenException

    return user


async def get_current_active_user(
    current_user: Annotated[UserData, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return current_user


async def user_admin(
    current_user: Annotated[UserData, Depends(get_current_active_user)],
) -> UserData:
    if not current_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions to view this section",
        )

    return current_user


async def user_powered(
    current_user: Annotated[UserData, Depends(get_current_active_user)],
) -> UserData:
    if not (current_user.role == "powered" or current_user.role == "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions to view this section",
        )

    return current_user
