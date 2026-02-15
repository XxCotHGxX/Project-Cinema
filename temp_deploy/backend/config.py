import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TMDB_API_KEY: str = ""
    TMDB_READ_ACCESS_TOKEN: str = ""
    STORAGE_HOST: str = "192.168.1.xxx"
    STORAGE_SHARE: str = "Videos"
    STORAGE_USER: str = "michael"
    STORAGE_PASS: str = ""
    SECRET_KEY: str = "cinema_secret_key_420"
    
    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

settings = Settings()
