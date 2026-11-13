from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Kreovio"
    environment: str = "development"
    log_level: str = "INFO"
    mongodb_uri: str = "mongodb://localhost:27018/?replicaSet=rs0"
    mongodb_database: str = "kreovio"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "development-only-change-me"
    fernet_key: str | None = None
    default_timezone: str = "Africa/Nairobi"
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2"
    llm_base_url: str = "http://localhost:11434"


@lru_cache
def get_settings() -> Settings:
    return Settings()

