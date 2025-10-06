from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str = Field(default='localhost')
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DATABASE: str = Field(default='postgres')
    POSTGRES_USER: str = Field(default='postgres')
    POSTGRES_PASSWORD: str = Field(default='1')

    TELEGRAM_BOT_TOKEN: str = Field()

    REDIS_URL: str = Field(default='redis://localhost:6379/1')

    JWT_SECRET_KEY: str = Field(default='secret')
    JWT_ALGORITHM: str = Field(default='HS256')
    JWT_ACCESS_TOKEN_EXPIRE_TIME: int = Field(default=60)
    JWT_REFRESH_TOKEN_EXPIRE_TIME: int = Field(default=3600)

    GEMINI_AI_API_KEY: str = Field()
    GEMINI_AI_MODEL: str = Field()
    AI_URL: str = Field()

    DEEPSEEK_AI_MODEL: str = Field()

    DEEPSEEK_AI_API_TOKEN: str = Field()

    UNSPLASH_ACCESS_KEY: str = Field()
    UNSPLASH_URL: str = Field()

    @property
    def postgres_sync_url(self):
        return (f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}")

    @property
    def postgres_async_url(self):
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}")

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")


settings = Settings()
# print(settings.GEMINI_AI_API_KEY,settings.AI_MODEL,settings.TELEGRAM_BOT_TOKEN)
