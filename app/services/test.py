from datetime import UTC, datetime

from app.core.collections import COL
from app.core.db import get_db
from app.schemas.test import TestCreate, TestResponse


async def create_test_document(data: TestCreate) -> TestResponse:
    document = {"message": data.message, "created_at": datetime.now(UTC)}
    result = await get_db()[COL.test].insert_one(document)
    return TestResponse(
        id=str(result.inserted_id),
        message=document["message"],
        created_at=document["created_at"],
    )
