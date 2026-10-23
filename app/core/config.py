import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "GreenPoints"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app/database/greenpoints.db")
    
    class Config:
        env_file = ".env"

settings = Settings()