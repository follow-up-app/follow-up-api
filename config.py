from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    PORT: int
    SQLALCHEMY_DATABASE_URI: str
    MONGO_DATABASE_URI: str
    DEBUG: bool = True
    SECRET_KEY: str = "3abc99c6afb0ae67124598af47e30f4bc907c395e239f9603b62b711c02dcd69"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600
    TESTING: bool = False
    APPLICATION_URL: str
    TIMEZONE: str = 'America/Sao_Paulo'
    POOL_RECYCLE: int = 3600
    API_MAIL: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_EMAIL_FROM: str
    SMTP_EMAIL_PASSWORD: str
    PANEL_URL: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
