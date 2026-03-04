import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env manually
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    REDIS_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()