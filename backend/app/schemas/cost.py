"""اسکیمای هزینه و خرید (issue #11, #12)."""
import uuid
from datetime import date

from pydantic import BaseModel

from app.models.cost import CostCategory, ProcurementStatus


class CostEntryCreate(BaseModel):
    project_id: uuid.UUID
    budget_id: uuid.UUID | None = None
    category: CostCategory
    description: str
    amount: float
    currency: str = "IRR"
    entry_date: date


class CostEntryOut(CostEntryCreate):
    id: uuid.UUID

    model_config = {"from_attributes": True}


class BudgetVarianceOut(BaseModel):
    budget_id: uuid.UUID
    category: CostCategory
    approved_amount: float
    spent_amount: float
    variance_amount: float
    variance_percent: float


class ProcurementItemCreate(BaseModel):
    project_id: uuid.UUID
    schedule_task_id: uuid.UUID | None = None
    item_name: str
    supplier: str | None = None
    quantity: float
    unit: str | None = None
    expected_delivery: date | None = None


class ProcurementItemOut(BaseModel):
    id: uuid.UUID
    item_name: str
    supplier: str | None
    quantity: float
    unit: str | None
    status: ProcurementStatus
    expected_delivery: date | None
    actual_delivery: date | None

    model_config = {"from_attributes": True}
