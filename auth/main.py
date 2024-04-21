from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

# from auth.api.v1 import roles, user, users
from auth.api.v1 import user
from auth.db.postgres import create_database
from auth.db.redis import redis


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # Импорт моделей необходим для их автоматического создания
    from auth.models.user import User  # noqa: F401
    from auth.services.jwt import get_config  # noqa: F401

    await create_database()
    await redis.initialize()
    yield
    await redis.close()


app = FastAPI(
    title="Change_to_var",  # TODO: change to variable
    docs_url="/api/openapi",
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    debug=True,
)

app.include_router(user.router, prefix="/api/v1/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # noqa: S104
