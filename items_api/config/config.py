# pylint: skip-file

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Items API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./items.db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
