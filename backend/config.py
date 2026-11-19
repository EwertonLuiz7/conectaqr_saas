from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "CONECTAQR"
    environment: str = "development"
    secret_key: str = "change-this-secret-key-before-production"
    database_url: str = "sqlite:///./conectaqr.db"
    base_url: str = "http://127.0.0.1:8000"
    access_token_expire_minutes: int = 1440

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
