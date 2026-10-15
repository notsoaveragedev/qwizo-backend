from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.responses import error_response


class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "INTERNAL_ERROR"
    message = "Something went wrong"

    def __init__(
        self, message: str | None = None, details: dict[str, Any] | None = None
    ) -> None:
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)


class BadRequestError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "BAD_REQUEST"
    message = "Invalid request"


class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "UNAUTHORIZED"
    message = "Please log in"


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "FORBIDDEN"
    message = "You don't have access"


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "NOT_FOUND"
    message = "Not found"


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "CONFLICT"
    message = "Already exists"


async def _app_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)
    return error_response(exc.status_code, exc.code, exc.message, exc.details)


async def _validation_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    if any(err["type"] == "json_invalid" for err in exc.errors()):
        return error_response(
            status.HTTP_400_BAD_REQUEST,
            "INVALID_JSON",
            "Request body is not valid JSON",
        )
    fields: dict[str, list[str]] = {}
    for err in exc.errors():
        field = ".".join(str(part) for part in err["loc"] if part != "body") or "body"
        fields.setdefault(field, []).append(err["msg"])
    return error_response(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        "VALIDATION_ERROR",
        "Some fields are invalid",
        {"fields": fields},
    )


async def _http_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    try:
        code = HTTPStatus(exc.status_code).name
    except ValueError:
        code = "HTTP_ERROR"
    return error_response(exc.status_code, code, str(exc.detail), headers=exc.headers)


# Uvicorn already logs the full traceback for unhandled errors; this only shapes the reply.
async def _unhandled_error(_: Request, __: Exception) -> JSONResponse:
    return error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", "Something went wrong"
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _app_error)
    app.add_exception_handler(RequestValidationError, _validation_error)
    app.add_exception_handler(StarletteHTTPException, _http_error)
    app.add_exception_handler(Exception, _unhandled_error)
