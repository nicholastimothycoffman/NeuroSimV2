from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@127.0.0.1:5433/neurosimv2"

    class Config:
        env_file = ".env"


settings = Settings()
