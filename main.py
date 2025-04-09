from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api import router
from app.config import settings
from app.db import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    await database.connect()
    print(f"Connected to PostgreSQL database using asyncpg driver")
    yield
    # Shutdown: Disconnect from the database
    await database.disconnect()
    print("Disconnected from PostgreSQL database")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    servers=[
        {
            "url": settings.SERVER_URL,
            "description": settings.SERVER_DESCRIPTION,
        }
    ],
    lifespan=lifespan,
)

app.include_router(router, prefix="/api", tags=["api"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI PostgreSQL application",
        "docs": "/docs",
    }
