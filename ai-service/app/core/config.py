from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    database_url: str = "postgresql+asyncpg://jobturn:jobturn@localhost:5432/jobturn"
    redis_url: str = "redis://localhost:6379"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    worknet_api_key: str = ""
    saramin_api_key: str = ""
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
