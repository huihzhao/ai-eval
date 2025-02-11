from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    PORT: int = 3000

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
