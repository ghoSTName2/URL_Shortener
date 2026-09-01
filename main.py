
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import Base, engine
from routers.shortener import router as url_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="URL Shortener API",
    description="Сервіс скорочення посилань на FastAPI та SQLAlchemy 2.0",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(url_router)

@app.get('/', tags=['Health'])
async def root():
    return {'message':'URL Shortener API is running'}