from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.api.cities import router as city_router
from app.api.dashboard import router as dashboard_router
from app.api.permissions import router as permission_router
from app.api.provinces import router as province_router
from app.api.roles import router as role_router
from app.api.users import router as user_router

from app.db.session import engine
from app.exceptions.handlers import register_exception_handlers


app = FastAPI(
    title="MAJE API",
    description="MAJE Backend API",
    version="1.0.0",
)


# =====================================
# Exception Handler
# =====================================

register_exception_handlers(app)


# =====================================
# Routers
# =====================================

# Authentication
app.include_router(auth_router)

# User Management
app.include_router(user_router)

# Master Data
app.include_router(province_router)
app.include_router(city_router)

# Dashboard
app.include_router(dashboard_router)

# RBAC
app.include_router(role_router)
app.include_router(permission_router)


# =====================================
# Root
# =====================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": "Welcome to MAJE API DEV",
    }


# =====================================
# Health Check
# =====================================

@app.get("/health")
def health():
    return {
        "success": True,
        "message": "MAJE API is running",
        "version": "1.0.0",
    }


@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "success": True,
            "message": "Database connected",
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }