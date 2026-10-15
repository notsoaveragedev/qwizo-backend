from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    app_name: str = "qwizo"
    env: Literal["development", "production"] = "development"
    api_prefix: str = "/api/v1"
    host: str = "127.0.0.1"
    port: int = 8000

    mongo_uri: SecretStr
    mongo_name: str = "qwizo"

    @property
    def is_production(self) -> bool:
        return self.env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
