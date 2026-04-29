from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CrossBorder AI Agent"
    database_url: str = "sqlite:///./crossborder_ai.db"
    ai_provider: str = "mock"
    zhipuai_api_key: str | None = None
    zhipuai_model: str = "glm-4-flash"
    feishu_webhook_url: str | None = None
    feishu_secret: str | None = None
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
