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

    def get_db_url(self):
        return f"sqlite+aiosqlite:///{Path(__file__).resolve().parent}/db/data.db"


settings = Settings()
