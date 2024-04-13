from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    """Настройки PostgreSQL."""

    model_config = SettingsConfigDict(extra="ignore")

    user: str = Field(..., alias="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD")
    db: str = Field("auth_db", alias="POSTGRES_DB")
    host: str = Field("127.0.0.1", alias="DB_HOST")
    port: int = Field(6379, alias="DB_PORT")


class RedisConfig(BaseSettings):
    """Настройки Redis."""

    model_config = SettingsConfigDict(extra="ignore")

    host: str = Field("127.0.0.1", alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")


env_file = ".env"
pg_config = PostgresConfig(_env_file=env_file)
redis_config = RedisConfig(_env_file=env_file)
