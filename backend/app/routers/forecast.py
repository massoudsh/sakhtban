"""روتر پیش‌بینی اثر زنجیره‌ای تأخیر (issue #13)."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.schedule import ScheduleTask, TaskDependency
from app.services.critical_path_forecast import forecast_delay_impact

router = APIRouter(prefix="/forecast", tags=["forecast"])


class DelayForecastRequest(BaseModel):
    schedule_task_id: uuid.UUID
    delay_days: int


class ForecastImpactOut(BaseModel):
    task_id: str
    task_name: str
    delay_days: int
    new_forecast_finish: str


@router.post("/{project_id}/delay-impact", response_model=list[ForecastImpactOut])
def delay_impact(project_id: uuid.UUID, payload: DelayForecastRequest, db: Session = Depends(get_db)) -> list[ForecastImpactOut]:
    tasks = list(db.scalars(select(ScheduleTask).where(ScheduleTask.project_id == project_id)))
    if not tasks:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "فعالیتی برای این پروژه یافت نشد.")

    task_ids = {t.id for t in tasks}
    dependencies = list(
        db.scalars(select(TaskDependency).where(TaskDependency.successor_id.in_(task_ids)))
    )

    impacts = forecast_delay_impact(
        tasks=tasks,
        dependencies=dependencies,
        source_task_id=str(payload.schedule_task_id),
        delay_days=payload.delay_days,
    )
    return [
        ForecastImpactOut(
            task_id=i.task_id,
            task_name=i.task_name,
            delay_days=i.delay_days,
            new_forecast_finish=i.new_forecast_finish.isoformat(),
        )
        for i in impacts
    ]
