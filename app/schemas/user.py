from datetime import datetime

from pydantic import BaseModel, Field

from app.db_base import str_req_uq, str_req


class User(BaseModel):
    username: str_req_uq
    role: str_req = "user"
    disabled: bool | None = None

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.username})"


class UserInDB(User):
    id: int
    password: str


class UserData(User):
    id: int
    created: datetime
    modified: datetime


class UserRegister(User):
    password: str_req = Field(
        min_length=5, max_length=15, description="Пароль пользователя"
    )


class UserLogin(BaseModel):
    username: str = Field(..., description="Имя пользователя")
    password: str = Field(
        ..., min_length=5, max_length=15, description="Пароль пользователя"
    )
