from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
