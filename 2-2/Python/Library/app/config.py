from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/library_db"
    DATABASE_TEST_URL: str = "postgresql://postgres:postgres@db:5432/library_test"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Library Management System"
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()