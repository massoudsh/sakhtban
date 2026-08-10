"""اسکیمای گزارش کارگاه (issue #1, #2, #6)."""
import uuid

from pydantic import BaseModel

from app.models.report import ReportChannel, ReportEntityType, ReportStatus


class SiteReportCreate(BaseModel):
    project_id: uuid.UUID
    channel: ReportChannel = ReportChannel.WEB
    raw_text: str
    report_date: str


class ReportEntityOut(BaseModel):
    entity_type: ReportEntityType
    value: str
    quantity: float | None = None
    unit: str | None = None
    confidence: float

    model_config = {"from_attributes": True}


class SiteReportOut(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    channel: ReportChannel
    raw_text: str
    report_date: str
    status: ReportStatus
    entities: list[ReportEntityOut] = []

    model_config = {"from_attributes": True}


class TelegramWebhookPayload(BaseModel):
    """ساختار ساده‌شده‌ی webhook تلگرام برای دریافت گزارش هفتگی (issue #6)."""

    message: dict
