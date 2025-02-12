from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import User, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./user/token")


# ==============================
# ==============================
def fake_hash_password(password: str):
    return f"fakehashed{password}"


def fake_decode_token(token):
    user = get_user(fake_users, token)

    return user


fake_users = {
    "johndoe": {
        "username": "johndoe",
        "hashedpwd": "fakehashedpassword",
        "role": "user",
        "disabled": False,
    },
    "janedoe": {
        "username": "janedoe",
        "hashedpwd": "fakehashedpassword1",
        "role": "user",
        "disabled": True,
    },
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]

        return UserInDB(**user_dict)


# ==============================
# ==============================


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return current_user
