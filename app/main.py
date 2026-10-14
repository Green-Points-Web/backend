
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db, get_db
from app.routes import catalog, dashboard, actions, points, history
from app.seed import seed_catalog



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with SessionLocal() as db:
        seed_catalog(db)
    yield


app = FastAPI(
    title="GreenPoints API",
    description="API to register sustainable actions and earn points.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


app.include_router(catalog.router)
app.include_router(dashboard.router)
app.include_router(actions.router)
app.include_router(history.router)
app.include_router(points.router)
