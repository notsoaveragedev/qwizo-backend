from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class SuccessResponse[T](BaseModel):
    success: bool = True
    message: str
    data: T | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    code: str
    details: dict[str, Any] = Field(default_factory=dict)


def success_response(
    data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    body = SuccessResponse[Any](message=message, data=data)
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json"))


def created_response(data: Any = None, message: str = "Created") -> JSONResponse:
    return success_response(data, message, status.HTTP_201_CREATED)


def error_response(
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    body = ErrorResponse(message=message, code=code, details=details or {})
    return JSONResponse(
        status_code=status_code, content=body.model_dump(mode="json"), headers=headers
    )
