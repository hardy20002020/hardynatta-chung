from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

app = FastAPI(
    title="MAJE API",
    description="MAJE Backend API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Welcome to MAJE API",
    }


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