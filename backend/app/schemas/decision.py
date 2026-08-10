"""اسکیمای Decision Log (issue #15-#20)."""
import uuid
from datetime import date

from pydantic import BaseModel

from app.models.decision import AmbiguityType, DecisionDocumentType, DecisionStatus


class DecisionDocumentCreate(BaseModel):
    project_id: uuid.UUID
    document_type: DecisionDocumentType
    title: str
    raw_text: str
    document_date: date | None = None


class AmbiguityFlagOut(BaseModel):
    ambiguity_type: AmbiguityType
    explanation: str
    risk_score: float

    model_config = {"from_attributes": True}


class DecisionOut(BaseModel):
    id: uuid.UUID
    statement: str
    responsible_party: str | None
    decision_date: date | None
    status: DecisionStatus
    financial_impact: float | None
    ambiguity_flags: list[AmbiguityFlagOut] = []

    model_config = {"from_attributes": True}


class DecisionDocumentOut(BaseModel):
    id: uuid.UUID
    document_type: DecisionDocumentType
    title: str
    document_date: date | None
    decisions: list[DecisionOut] = []

    model_config = {"from_attributes": True}
