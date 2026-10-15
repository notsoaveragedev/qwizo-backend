from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.db import close_mongo, connect_mongo, ping_mongo
from app.router.router import api_router
from app.utils.exceptions import register_exception_handlers
from app.utils.responses import error_response, success_response

settings = get_settings()
show_docs = not settings.is_production


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    await connect_mongo()
    yield
    await close_mongo()


app = FastAPI(
    title=f"{settings.app_name} API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if show_docs else None,
    redoc_url="/redoc" if show_docs else None,
    openapi_url="/openapi.json" if show_docs else None,
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect" if show_docs else None,
)

register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health")
async def health() -> JSONResponse:
    return success_response({"env": settings.env}, "Service is running")


@app.get("/ready")
async def ready() -> JSONResponse:
    if not await ping_mongo():
        return error_response(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "SERVICE_UNAVAILABLE",
            "Database unreachable",
        )
    return success_response({"mongo": "ok"}, "Ready")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=not settings.is_production,
    )
