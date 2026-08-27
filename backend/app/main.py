import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.core import RateLimitMiddleware
from app.database import init_db
from app.routes import (
    auth, careers, skills, dashboard, jobs, study, resources,
    projects, interviews, resume, market, notifications, profile,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("careerpath")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="CareerPath AI — choose a tech career, master the skill DAG, close job gaps.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(RateLimitMiddleware, max_requests=300, window_seconds=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Never leak internals to clients
    logger.exception("Unhandled error on %s: %s", request.url.path, exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# ---- API v1 ----
API = "/api/v1"
app.include_router(auth.router, prefix=API)
app.include_router(careers.router, prefix=API)
app.include_router(skills.router, prefix=API)
app.include_router(dashboard.router, prefix=API)
app.include_router(jobs.router, prefix=API)
app.include_router(study.router, prefix=API)
app.include_router(resources.router, prefix=API)
app.include_router(projects.router, prefix=API)
app.include_router(interviews.router, prefix=API)
app.include_router(resume.router, prefix=API)
app.include_router(market.router, prefix=API)
app.include_router(notifications.router, prefix=API)
app.include_router(profile.router, prefix=API)


@app.on_event("startup")
def on_startup():
    init_db()
    try:
        from app.seed.seeder import run_seed
        summary = run_seed()
        logger.info("Seed complete: %s", summary["careers"])
    except Exception:
        logger.exception("Seeding failed — continuing with existing data")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}


# ---- Static Frontend Mounting ----
DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))

if os.path.exists(DIST_DIR):
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(DIST_DIR, "index.html"))

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        if full_path.startswith(("api", "docs", "redoc", "openapi.json")):
            return JSONResponse(status_code=404, content={"detail": "Not found"})
        file_path = os.path.join(DIST_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(DIST_DIR, "index.html"))
