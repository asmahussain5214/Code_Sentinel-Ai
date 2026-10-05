from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.db.base_class import Base
from app.db.session import engine

load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)

from app import models  # noqa: E402,F401


app = FastAPI(
    title="CodeSentinel AI"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(
        bind=engine
    )


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


app.include_router(
    api_router,
    prefix="/api/v1"
)
Base.metadata.create_all(bind=engine)