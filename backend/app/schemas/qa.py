"""اسکیمای QA Copilot (issue #21-#26)."""
import uuid
from datetime import date

from pydantic import BaseModel

from app.models.qa import DefectSeverity, DefectStatus, PunchItemStatus


class DefectCreate(BaseModel):
    """ثبت ایراد از اپ موبایل: عکس + موقعیت + توضیح (issue #22)."""

    project_id: uuid.UUID
    contractor_name: str | None = None
    title: str
    description: str
    category: str | None = None
    location: str
    photo_before_url: str | None = None
    gps_lat: float | None = None
    gps_lng: float | None = None
    severity: DefectSeverity = DefectSeverity.MINOR
    due_date: date | None = None


class DefectOut(BaseModel):
    id: uuid.UUID
    contractor_name: str | None
    title: str
    description: str
    category: str | None
    location: str
    photo_before_url: str | None
    photo_after_url: str | None
    severity: DefectSeverity
    status: DefectStatus
    reopened_count: int
    due_date: date | None

    model_config = {"from_attributes": True}


class DefectFixSubmit(BaseModel):
    """پیمانکار عکس بعد از اصلاح را ثبت می‌کند -> وضعیت به fixed می‌رود."""

    photo_after_url: str


class DefectVerify(BaseModel):
    """ناظر اصلاح را تأیید (verified) یا رد (reopened -> افزایش rework) می‌کند."""

    approved: bool


class PunchItemOut(BaseModel):
    id: uuid.UUID
    defect_id: uuid.UUID
    status: PunchItemStatus
    closed_at: date | None

    model_config = {"from_attributes": True}


class ReworkPatternOut(BaseModel):
    dimension: str
    dimension_value: str
    defect_count: int
    reopened_count: int
    rework_rate: float
    is_alert: bool
