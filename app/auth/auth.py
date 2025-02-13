from datetime import timedelta, datetime, timezone

from passlib.context import CryptContext
import jwt

from app.config import get_auth_token_data
from app.schemas.user import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY, ALGORITHM, EXPIRE = get_auth_token_data().values()

# ===========================================================
# ===========================================================
fake_users = {
    "johndoe": {
        "username": "johndoe",
        "hashedpwd": "$2b$12$DToGEUZw1YTLEztOEAfosudAAjNScrye58N/NB1P/Fe4lwDXg9wcK",
        "role": "user",
        "disabled": False,
    },
    "janedoe": {
        "username": "janedoe",
        "hashedpwd": "$2b$12$4HTB4sulmwJMRPeEbKV7sebp3n2xNbDldo69DMtp2RHipfl8eAOb6",
        "role": "user",
        "disabled": True,
    },
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]

        return UserInDB(**user_dict)


# ===========================================================
# ===========================================================


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# TODO: При испорльзовании базы данных для аутентификации пользоывтеля использовать асинхронную функцию с запросом к базе данных
def authenticate_user(fake_users, username: str, password: str):
    user = get_user(fake_users, username)

    if not user:
        return False

    if not verify_password(password, user.hashedpwd):
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
