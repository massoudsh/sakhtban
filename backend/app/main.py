"""نقطه‌ی ورود اپلیکیشن FastAPI — Sakhtban API."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.routers import (
    auth,
    cost,
    decisions,
    deviations,
    forecast,
    onboarding,
    projects,
    qa,
    reports,
    reports_exec,
    risk,
    schedule,
    uploads,
)

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
app.mount(settings.upload_public_path, StaticFiles(directory=settings.upload_dir), name="uploaded-files")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(reports.router)
app.include_router(schedule.router)
app.include_router(deviations.router)
app.include_router(deviations.action_router)
app.include_router(risk.router)
app.include_router(cost.router)
app.include_router(cost.procurement_router)
app.include_router(forecast.router)
app.include_router(decisions.router)
app.include_router(qa.router)
app.include_router(uploads.router)
app.include_router(reports_exec.router)
app.include_router(onboarding.router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "app": settings.app_name}
