from fastapi import APIRouter

from app.controllers import test

api_router = APIRouter()
api_router.include_router(test.router)
