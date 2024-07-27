import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./news_aggregator.db")
    NEWS_SOURCE_URL: str = os.getenv("NEWS_SOURCE_URL")
    LOG_FILE: str = "logs/news_aggregator.log"
    HEROKU_API_KEY: str = os.getenv("HEROKU_API_KEY")
    CLOUDAMQP_URL: str = os.getenv("CLOUDAMQP_URL")

    class Config:
        env_file = ".env"

settings = Settings()