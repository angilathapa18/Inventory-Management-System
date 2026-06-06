from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import categories, items, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: run Alembic migrations or create tables for dev only
    yield


app = FastAPI(
    title="Inventory & Asset Management System",
    description="REST API for inventory, assets, and transactions",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(categories.router)
app.include_router(users.router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
