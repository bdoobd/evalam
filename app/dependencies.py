from typing import Annotated

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.schemas.user import User
from app.auth.auth import decode_access_token
from app.schemas.token import TokenData
from app.dao.user import UserDAO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./user/token")


def get_token(request: Request):
    token = request.cookies.get("pass_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен доступа не найден"
        )

    return token


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
async def get_current_user(token: Annotated[str, Depends(get_token)]):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Аутетификация пользователя не возможна",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")

        if username is None:
            raise cred_exception

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise cred_exception

    user = await UserDAO.find_user({"username": token_data.username})

    if user is None:
        raise cred_exception

    return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
#         )

#     return current_user
