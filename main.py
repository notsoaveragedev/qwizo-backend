import uvicorn
from fastapi import FastAPI

from app.controllers.health import health
from app.router.router import api_router
from app.core.config import get_settings

settings = get_settings()
show_docs = not settings.is_production

app = FastAPI(
    title="Qwizo",
    version="0.1.0",
    docs_url="/docs" if show_docs else None,
    redoc_url="/redoc" if show_docs else None,
    openapi_url="/openapi.json" if show_docs else None,
    description="Qwizo is a platform that allows users to create and share quizzes with others. Users can create quizzes on any topic, and share them with friends or the public. Users can also take quizzes created by others, and see how they rank against other users."
)

app.include_router(health.router)
app.include_router(api_router,prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=not settings.is_production,port=settings.port,host="0.0.0.0")