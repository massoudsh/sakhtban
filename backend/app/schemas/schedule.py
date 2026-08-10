"""اسکیمای برنامه‌ی زمان‌بندی (issue #9, #10)."""
import uuid
from datetime import date

from pydantic import BaseModel

from app.models.schedule import TaskStatus


class ScheduleTaskOut(BaseModel):
    id: uuid.UUID
    external_task_id: str
    name: str
    wbs_path: str | None
    baseline_start: date | None
    baseline_finish: date | None
    actual_start: date | None
    actual_finish: date | None
    forecast_finish: date | None
    percent_complete: float
    status: TaskStatus

    model_config = {"from_attributes": True}


class ScheduleImportOut(BaseModel):
    id: uuid.UUID
    source: str
    original_filename: str
    is_baseline: bool
    task_count: int

    model_config = {"from_attributes": True}
