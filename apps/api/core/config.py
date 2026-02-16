from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Open-Scribe-AI"
    env: str = "dev"
    log_level: str = "INFO"

    phi_safe_logging: bool = True
    require_api_key: bool = False
    api_key: str = ""

    ollama_base_url: str = "http://ollama:11434"
    llm_model: str = "llama3.1:8b"
    llm_timeout_seconds: int = 45
    allow_cloud_llm: bool = False

    whisper_model: str = Field(default="tiny")
    deidentify_default: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
