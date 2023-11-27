from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import validator, PostgresDsn
from typing import Any, Optional, Dict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@postgres/postgres"

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(self, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql" + "+psycopg2",
    #         username=values.get("POSTGRES_USER") or "postgres",
    #         password=values.get("POSTGRES_PASSWORD") or "postgres",
    #         host=values.get("POSTGRES_HOST") or "postgres",
    #         path=f"/{values.get('POSTGRES_DATABASE') or 'postgres'}",
    #         port=values.get("POSTGRES_PORT" or "5432"),
    #     )


settings = Settings()
