import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "GreenPoints"
    # Ruta por defecto a la base de datos SQLite
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app/database/greenpoints.db")
    
    class Config:
        env_file = ".env"

settings = Settings()