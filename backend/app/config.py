from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # SQLite stores the database in a local file; no separate DB server needed.
    database_url: str = "sqlite:///./creatorx.db"
    jwt_secret: str = "change-me"
    jwt_expire_minutes: int = 60 * 24
    cors_origins: str = "http://localhost:3000"


settings = Settings()
