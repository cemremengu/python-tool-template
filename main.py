import uvicorn
from fastapi import FastAPI

from app.api import items
from app.config import settings
from app.db import database

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Include the API endpoints directly
app.include_router(items.router, prefix="/api/items", tags=["items"])

# You can add more endpoint modules directly here
# app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.on_event("startup")
async def startup():
    # Connect to the database (Oracle or PostgreSQL based on configuration)
    await database.connect()
    print(
        f"Connected to {settings.DB_TYPE} database using {'asyncpg' if settings.DB_TYPE == 'postgresql' else 'oracledb'} driver"
    )


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print(f"Disconnected from {settings.DB_TYPE} database")


@app.get("/")
async def root():
    return {
        "message": f"Welcome to the FastAPI {settings.DB_TYPE.capitalize()} application",
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
