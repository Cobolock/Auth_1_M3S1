from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = ".env"


class PostgresConfig(BaseSettings):
    """Настройки PostgreSQL."""

    model_config = SettingsConfigDict(extra="ignore")

    user: str = Field(..., alias="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD")
    db: str = Field("auth_db", alias="POSTGRES_DB")
    host: str = Field("127.0.0.1", alias="DB_HOST")
    port: int = Field(5432, alias="DB_PORT")


class RedisConfig(BaseSettings):
    """Настройки Redis."""

    model_config = SettingsConfigDict(extra="ignore")

    host: str = Field("127.0.0.1", alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")


class ExtraConfig(BaseSettings):
    """Прочие настройки."""

    model_config = SettingsConfigDict(extra="ignore")

    salt: str = Field(..., alias="SALT")


class JWTSettings(BaseSettings):
    """Параметры конфигурации JWT."""

    model_config = SettingsConfigDict(extra="ignore", env_file=env_file)

    authjwt_secret_key: str = Field(..., alias="JWT_SECRET")


pg_config = PostgresConfig(_env_file=env_file)
redis_config = RedisConfig(_env_file=env_file)
extra_config = ExtraConfig(_env_file=env_file)
