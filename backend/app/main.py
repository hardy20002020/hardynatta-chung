from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as user_router


# ==========================================================
# FASTAPI APPLICATION
# ==========================================================

app = FastAPI(
    title="MAJE API",
    description="MAJE Backend API",
    version="1.1.0",
)


# ==========================================================
# CORS CONFIGURATION
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # React / Vite Development
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# API ROUTERS
# ==========================================================

app.include_router(auth_router)
app.include_router(user_router)


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": "MAJE API Running",
    }