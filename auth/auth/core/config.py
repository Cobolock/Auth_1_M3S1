import sys

from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    """Настройки PostgreSQL."""

    model_config = SettingsConfigDict(extra="ignore")

    dialect: str = "postgresql"
    driver: str = "asyncpg"
    user: SecretStr = Field(..., alias="POSTGRES_USER")
    password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    db: str = Field("auth_db", alias="POSTGRES_DB")
    host: str = Field("127.0.0.1", alias="DB_HOST")
    port: int = Field(5432, alias="DB_PORT")
    echo: str = Field("True", alias="DB_ECHO")

    @property
    def dsn(self) -> str:
        return (
            f"{self.dialect}+{self.driver}://{self.user.get_secret_value()}:"
            f"{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"
        )


class RedisConfig(BaseSettings):
    """Настройки Redis."""

    model_config = SettingsConfigDict(extra="ignore")

    host: str = Field("127.0.0.1", alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")


class ExtraConfig(BaseSettings):
    """Прочие настройки."""

    model_config = SettingsConfigDict(extra="ignore")

    salt: str = Field(..., alias="SALT")
    enable_tracer: bool = Field(False, alias="ENABLE_TRACER")
    enable_rate_limiter: bool = Field(False, alias="ENABLE_RATE_LIMITER")


class JWTSettings(BaseSettings):
    """Параметры конфигурации JWT."""

    model_config = SettingsConfigDict(extra="ignore")
    authjwt_secret_key: str = Field(..., alias="JWT_SECRET")


class JaegerSettings(BaseSettings):
    """Настройки Jaeger."""

    model_config = SettingsConfigDict(extra="ignore")

    console_output: bool = Field(False, alias="JAEGER_CONSOLE_OUTPUT")
    agent_host: str | None = Field(None, alias="JAEGER_AGENT_HOST")
    agent_port: int | None = Field(None, alias="JAEGER_AGENT_PORT")


class RateLimitSettings(BaseSettings):
    """Настройки лимитов запросов."""

    model_config = SettingsConfigDict(extra="ignore")

    max_requests: int = Field(100, alias="RATE_LIMIT_MAX_REQUESTS")
    period_seconds: int = Field(60, alias="RATE_LIMIT_PERIOD_SECONDS")


class YandexAuthSettings(BaseSettings):
    """Настройки для подключения приложения к Яндекс ID."""

    model_config = SettingsConfigDict(extra="ignore")

    yandex_client_id: str = Field(..., alias="YANDEX_CLIENT_ID")
    yandex_client_secret: str = Field(..., alias="YANDEX_CLIENT_SECRET")
    yandex_redirect_uri: str = Field(..., alias="YANDEX_REDIRECT_URI")


env_path = Path(__file__).parent.parent.parent / "envs"
env_filename = ".env.test" if "pytest" in sys.modules else ".env"
env_file = env_path / env_filename

pg_config = PostgresConfig(_env_file=env_file)
redis_config = RedisConfig(_env_file=env_file)
extra_config = ExtraConfig(_env_file=env_file)
jwt_settings = JWTSettings(_env_file=env_file)
jaeger_settings = JaegerSettings(_env_file=env_file)
rate_limit_settings = RateLimitSettings(_env_file=env_file)
yandex_auth_settings = YandexAuthSettings(_env_file=env_file)
