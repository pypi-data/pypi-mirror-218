from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseModel):
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings():
    settings = Settings()
    return settings
