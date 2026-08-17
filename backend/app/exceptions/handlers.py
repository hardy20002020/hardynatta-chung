import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.base import ApiResponse


logger = logging.getLogger("maje.exceptions")


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        logger.warning(
            "HTTP exception: method=%s path=%s status=%s",
            request.method,
            request.url.path,
            exc.status_code,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse(
                success=False,
                message=str(exc.detail),
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        logger.warning(
            "Request validation failed: method=%s path=%s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=422,
            content=ApiResponse(
                success=False,
                message="Validation failed",
                data=None,
                errors=exc.errors(),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "Unhandled exception: method=%s path=%s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=500,
            content=ApiResponse(
                success=False,
                message="Internal Server Error",
                data=None,
            ).model_dump(),
        )