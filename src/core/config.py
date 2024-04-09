from dataclasses import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

settings = BaseSettings()

load_dotenv()


class PostgresSettings(BaseSettings):
    user: str = Field(..., alias='POSTGRES_USER')
    password: str = Field(..., alias='POSTGRES_PASSWORD')
    db: str = Field('auth_db', alias='POSTGRES_DB')
    host: str = Field('127.0.0.1', alias='DB_HOST')
    port: int = Field(6379, alias='DB_PORT')


class RedisConfig(BaseSettings):
    """Настройки Redis"""
    host: str = Field('127.0.0.1', env='REDIS_HOST')
    port: int = Field(6379, env='REDIS_PORT')

pg_config = PostgresSettings()
redis_config = RedisConfig()