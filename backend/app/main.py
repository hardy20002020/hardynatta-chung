from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security_headers import SecurityHeadersMiddleware

from app.exceptions.handlers import register_exception_handlers

from app.api.auth import router as auth_router
from app.api.users import router as user_router
from app.api.provinces import router as province_router
from app.api.cities import router as city_router
from app.api.dashboard import router as dashboard_router
from app.api.roles import router as role_router
from app.api.permissions import router as permission_router
from app.api.role_permissions import router as role_permission_router
from app.api.audit_logs import router as audit_log_router
from app.api.competitions import router as competition_router
from app.api.competition_groups import (
    router as competition_group_router,
)


# ==========================================================
# FASTAPI APPLICATION
# ==========================================================

app = FastAPI(
    title="MAJE API",
    description="MAJE Backend API",
    version="1.1.0",
    docs_url=(
        "/docs"
        if settings.api_docs_enabled
        else None
    ),
    redoc_url=(
        "/redoc"
        if settings.api_docs_enabled
        else None
    ),
    openapi_url=(
        "/openapi.json"
        if settings.api_docs_enabled
        else None
    ),
)


# ==========================================================
# RATE LIMIT SECURITY
# ==========================================================

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


# ==========================================================
# EXCEPTION HANDLING
# ==========================================================

register_exception_handlers(app)


# ==========================================================
# TRUSTED HOST SECURITY
# ==========================================================

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts,
)


# ==========================================================
# SECURITY HEADERS
# ==========================================================

app.add_middleware(
    SecurityHeadersMiddleware,
)


# ==========================================================
# CORS CONFIGURATION
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=settings.cors_allowed_methods,
    allow_headers=settings.cors_allowed_headers,
)


# ==========================================================
# API ROUTERS
# ==========================================================

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(province_router)
app.include_router(city_router)
app.include_router(dashboard_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(role_permission_router)
app.include_router(audit_log_router)
app.include_router(competition_router)
app.include_router(competition_group_router)


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health():
    return {
        "success": True,
        "message": "MAJE healthy",
    }


# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": "MAJE API Running",
    }