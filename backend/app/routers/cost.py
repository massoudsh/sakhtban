"""روتر هزینه و خرید (issue #11, #12)."""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.cost import Budget, CostEntry, ProcurementItem
from app.schemas.cost import (
    BudgetVarianceOut,
    CostEntryCreate,
    CostEntryOut,
    ProcurementItemCreate,
    ProcurementItemOut,
)

router = APIRouter(prefix="/costs", tags=["costs"])


@router.post("", response_model=CostEntryOut, status_code=status.HTTP_201_CREATED)
def create_cost_entry(payload: CostEntryCreate, db: Session = Depends(get_db)) -> CostEntry:
    entry = CostEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/{project_id}", response_model=list[CostEntryOut])
def list_cost_entries(project_id: uuid.UUID, db: Session = Depends(get_db)) -> list[CostEntry]:
    stmt = select(CostEntry).where(CostEntry.project_id == project_id)
    return list(db.scalars(stmt))


@router.get("/{project_id}/variance", response_model=list[BudgetVarianceOut])
def budget_variance(project_id: uuid.UUID, db: Session = Depends(get_db)) -> list[BudgetVarianceOut]:
    """انحراف هزینه‌ی واقعی نسبت به بودجه‌ی مصوب، به‌تفکیک ردیف بودجه."""
    budgets = list(db.scalars(select(Budget).where(Budget.project_id == project_id)))
    results = []
    for budget in budgets:
        spent = db.scalar(
            select(func.coalesce(func.sum(CostEntry.amount), 0)).where(CostEntry.budget_id == budget.id)
        )
        spent_amount = float(spent or 0)
        approved = float(budget.approved_amount)
        variance_amount = spent_amount - approved
        variance_percent = (variance_amount / approved * 100) if approved else 0.0
        results.append(
            BudgetVarianceOut(
                budget_id=budget.id,
                category=budget.category,
                approved_amount=approved,
                spent_amount=spent_amount,
                variance_amount=variance_amount,
                variance_percent=round(variance_percent, 2),
            )
        )
    return results


procurement_router = APIRouter(prefix="/procurement", tags=["procurement"])


@procurement_router.post("", response_model=ProcurementItemOut, status_code=status.HTTP_201_CREATED)
def create_procurement_item(payload: ProcurementItemCreate, db: Session = Depends(get_db)) -> ProcurementItem:
    item = ProcurementItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@procurement_router.get("/{project_id}", response_model=list[ProcurementItemOut])
def list_procurement_items(project_id: uuid.UUID, db: Session = Depends(get_db)) -> list[ProcurementItem]:
    stmt = select(ProcurementItem).where(ProcurementItem.project_id == project_id)
    return list(db.scalars(stmt))


@procurement_router.get("/{project_id}/delayed", response_model=list[ProcurementItemOut])
def list_delayed_items(project_id: uuid.UUID, db: Session = Depends(get_db)) -> list[ProcurementItem]:
    from datetime import date

    stmt = select(ProcurementItem).where(
        ProcurementItem.project_id == project_id,
        ProcurementItem.actual_delivery.is_(None),
        ProcurementItem.expected_delivery < date.today(),
    )
    return list(db.scalars(stmt))
