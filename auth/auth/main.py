from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from auth.api.v1.login_history import router as login_history_router
from auth.api.v1.permissions import router as permissions_router
from auth.api.v1.roles import router as roles_router
from auth.api.v1.user_auth import router as user_auth_router
from auth.api.v1.user_roles import router as user_roles_router
from auth.db.redis import redis


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await redis.initialize()
    yield
    await redis.close()


app = FastAPI(
    title="Auth API",
    docs_url="/api/docs",
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    debug=True,
)
app.include_router(permissions_router, prefix="/api/v1/permissions", tags=["Ограничения"])
app.include_router(roles_router, prefix="/api/v1/roles", tags=["Роли"])
app.include_router(login_history_router, prefix="/api/v1/user", tags=["История входов"])
app.include_router(user_auth_router, prefix="/api/v1/user", tags=["Пользователь"])
app.include_router(user_roles_router, prefix="/api/v1/users", tags=["Пользователи"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # noqa: S104
