from pydantic import BaseModel


class User(BaseModel):
    username: str
    role: str = "user"
    disabled: bool | None = None


class UserInDB(User):
    hashedpwd: str
