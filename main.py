from fastapi import FastAPI

from app.controllers.health import health
from app.router.router import api_router

app = FastAPI(title="Qwizo")

app.include_router(health.router)
app.include_router(api_router,prefix="/api/v1")