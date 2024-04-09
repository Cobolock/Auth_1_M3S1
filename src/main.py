from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis import Redis
from core.config import redis_config
from db import redis
from db.postgres import create_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Импорт моделей необходим для их автоматического создания
    from models.entity import User
    await create_database()

    redis.redis = Redis(
        host=redis_config.host,
        port=redis_config.port
    )
    yield

app = FastAPI(
    title='Change_to_var',
    docs_url='/api/openapi',
    lifespan=lifespan,
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    debug=True,
)
