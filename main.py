from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import Base, engine
from api.v1.router import router as v1_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    Base.metadata.create_all(bind=engine)

    yield
    # shutdown

app = FastAPI(
    title="Notes API",
    description="""
    REST API for a notes application.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(v1_router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "error": False,
        "result": {
            "status": "healthy",
            "application": "Notes API"
        },
        "message": "Application is running"
    }

frontend_dir = Path(__file__).parent / "static"

app.mount(
    "/webui",
    StaticFiles(directory=frontend_dir, html=True),
    name="frontend"
)

