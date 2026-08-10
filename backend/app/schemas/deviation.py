"""اسکیمای انحراف، action item و ریسک (issue #3, #4, #5)."""
import uuid

from pydantic import BaseModel

from app.models.deviation import ActionItemStatus, DeviationSeverity, DeviationType, RiskSourceType


class DeviationOut(BaseModel):
    id: uuid.UUID
    deviation_type: DeviationType
    severity: DeviationSeverity
    variance_days: int | None
    variance_percent: float | None
    description: str

    model_config = {"from_attributes": True}


class ActionItemOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: ActionItemStatus
    due_date: str | None

    model_config = {"from_attributes": True}


class ActionItemUpdate(BaseModel):
    status: ActionItemStatus | None = None
    assignee_id: uuid.UUID | None = None
    due_date: str | None = None


class RiskItemOut(BaseModel):
    id: uuid.UUID
    source_type: RiskSourceType
    title: str
    location: str | None
    severity_score: float
    likelihood_score: float
    is_resolved: bool

    model_config = {"from_attributes": True}
