from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import SessionLocal, init_db
from .routers import catalog
from .seed import seed_catalog
from .routes import dashboard



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with SessionLocal() as db:
        seed_catalog(db)
    yield


app = FastAPI(title="GreenPoints API", lifespan=lifespan)

app.include_router(catalog.router)
app.include_router(dashboard.router)