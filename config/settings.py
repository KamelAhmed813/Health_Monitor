from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="HEALTH_",
        case_sensitive=False,
    )

    # Auth
    jwt_secret: str = Field(default="change-me-in-prod", description="JWT signing secret")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_exp_minutes: int = Field(default=60)

    # Storage / caching
    redis_url: str = Field(default="redis://localhost:6379/0")
    sqlite_path: str = Field(default="backend/data/health.sqlite")

    # Google GenAI
    google_genai_api_key: str = Field(default="", description="Google GenAI API key")

    # Logging (consumed by config/logging.py)
    log_level: str = Field(default="INFO")


settings = Settings()

