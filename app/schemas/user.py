from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.dao.db_base import str_req_uq, str_req


class User(BaseModel):
    username: str_req_uq
    role: str_req = "user"
    disabled: bool = False

    model_config = ConfigDict(from_attributes=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.username})"


class UserInDB(User):
    id: int
    password: str


class UserData(User):
    id: int


class UserRegister(User):
    password: str_req = Field(
        min_length=5, max_length=15, description="Пароль пользователя"
    )
    confirm_password: str_req = Field(
        min_length=5, max_length=15, description="Подтверждение пароля пользователя"
    )


class UserLogin(BaseModel):
    username: str = Field(..., description="Имя пользователя")
    password: str = Field(
        ..., min_length=5, max_length=15, description="Пароль пользователя"
    )


class FindUser(BaseModel):
    username: str
