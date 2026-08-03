from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add baseline security headers to every HTTP response.

    Normal API endpoints receive a restrictive CSP.

    Swagger UI and ReDoc receive a documentation-specific
    CSP so their required scripts and styles can load during
    development while the rest of the API remains locked down.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        response = await call_next(request)

        # ======================================================
        # BASE SECURITY HEADERS
        # ======================================================

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        response.headers[
            "X-Frame-Options"
        ] = "DENY"

        response.headers[
            "Referrer-Policy"
        ] = "no-referrer"

        response.headers[
            "Permissions-Policy"
        ] = (
            "camera=(), "
            "microphone=(), "
            "geolocation=()"
        )

        # ======================================================
        # CONTENT SECURITY POLICY
        # ======================================================

        documentation_paths = {
            "/docs",
            "/redoc",
        }

        if request.url.path in documentation_paths:

            # FastAPI Swagger UI currently contains a small
            # inline initialization script. The hash permits
            # only that exact script instead of allowing all
            # inline JavaScript.
            response.headers[
                "Content-Security-Policy"
            ] = (
                "default-src 'self'; "
                "script-src 'self' "
                "https://cdn.jsdelivr.net "
                "'sha256-QOOQu4W1oxGqd2nbXbxiA1Di6OHQOLQD+o+G9oWL8YY='; "
                "style-src 'self' 'unsafe-inline' "
                "https://cdn.jsdelivr.net; "
                "img-src 'self' data: "
                "https://fastapi.tiangolo.com; "
                "connect-src 'self'; "
                "font-src 'self' data:; "
                "frame-ancestors 'none'"
            )

        else:

            # API responses do not require browser scripts,
            # styles, images, frames, or external resources.
            response.headers[
                "Content-Security-Policy"
            ] = (
                "default-src 'none'; "
                "frame-ancestors 'none'"
            )

        # ======================================================
        # HSTS - PRODUCTION ONLY
        # ======================================================

        if (
            settings.ENVIRONMENT.strip().lower()
            == "production"
        ):
            response.headers[
                "Strict-Transport-Security"
            ] = (
                "max-age=31536000; "
                "includeSubDomains"
            )

        return response