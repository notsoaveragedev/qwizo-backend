from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    env: Literal["development", "production"] = "development"
    api_prefix: str = "/api/v1"
    log_level: str = "INFO"
    mongo_uri: str
    mongo_name: str
    cors_origins: list[str] = ["http://localhost:3000"]
    port: int = 8001
    host: str = ""

    @property
    def is_production(self) -> bool:
        return self.env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
