from fastapi import FastAPI

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