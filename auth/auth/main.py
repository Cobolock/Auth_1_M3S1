import sys

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn

from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

from auth.api.v1.login_history import router as login_history_router
from auth.api.v1.permissions import router as permissions_router
from auth.api.v1.roles import router as roles_router
from auth.api.v1.user_auth import router as user_auth_router
from auth.api.v1.user_roles import router as user_roles_router
from auth.core.config import rate_limit_settings
from auth.core.tracing import tracer_provider
from auth.db.redis import redis


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await redis.initialize()
    await FastAPILimiter.init(redis)
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
app.add_middleware(
    OpenTelemetryMiddleware,  # type: ignore[arg-type]
    tracer_provider=tracer_provider,
    http_capture_headers_server_request=["X-Request-Id"],
)

dependencies = []
if "pytest" not in sys.modules:
    dependencies.append(
        Depends(
            RateLimiter(
                times=rate_limit_settings.max_requests, seconds=rate_limit_settings.period_seconds
            )
        )
    )
api_router = APIRouter(prefix="/api/v1", dependencies=dependencies)
api_router.include_router(permissions_router, prefix="/permissions", tags=["Ограничения"])
api_router.include_router(roles_router, prefix="/roles", tags=["Роли"])
api_router.include_router(login_history_router, prefix="/user", tags=["История входов"])
api_router.include_router(user_auth_router, prefix="/user", tags=["Пользователь"])
api_router.include_router(user_roles_router, prefix="/users", tags=["Пользователи"])
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # noqa: S104
