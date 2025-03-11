from datetime import timedelta, datetime, timezone

from passlib.context import CryptContext
import jwt

from app.config import get_auth_token_data

# from app.schemas.user import UserInDB
from app.dao.user import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY, ALGORITHM, EXPIRE = get_auth_token_data().values()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await UserDAO.find_user(username=username)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
