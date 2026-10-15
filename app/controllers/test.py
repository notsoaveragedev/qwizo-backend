from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.test import TestCreate, TestResponse
from app.services import test as test_service
from app.utils.responses import SuccessResponse, created_response

router = APIRouter(prefix="/test", tags=["test"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[TestResponse],
)
async def create_test(data: TestCreate) -> JSONResponse:
    test = await test_service.create_test_document(data)
    return created_response(test, "Test document created")
