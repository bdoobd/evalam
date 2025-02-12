from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
    )

    DB_USER: str
    DB_PWD: str
    DB_HOST: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MIN: int

    def get_db_url(self):
        return f"sqlite+aiosqlite:///{Path(__file__).resolve().parent}/db/data.db"


settings = Settings()


def get_auth_token_data():
    return {
        "secret_key": settings.SECRET_KEY,
        "algorithm": settings.ALGORITHM,
        "expires": settings.ACCESS_TOKEN_EXPIRES_MIN,
    }
