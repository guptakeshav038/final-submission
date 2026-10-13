from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine
from .routers import auth, campaigns, creators, matches


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)  # database/schema.sql is the same schema, for manual setup
    yield


app = FastAPI(title="CreatorX API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (auth, creators, campaigns, matches):
    app.include_router(r.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
