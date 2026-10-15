from datetime import datetime

from pydantic import BaseModel, Field


class TestCreate(BaseModel):
    message: str = Field(default="hello from qwizo", min_length=1, max_length=200)


class TestResponse(BaseModel):
    id: str
    message: str
    created_at: datetime
