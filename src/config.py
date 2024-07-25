import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./news_aggregator.db")
    NEWS_SOURCE_URL: str = "https://lithosgraphein.com/"
    LOG_FILE: str = "logs/news_aggregator.log"
    HEROKU_API_KEY: str = os.getenv("HEROKU_API_KEY")

    class Config:
        env_file = ".env"

settings = Settings()