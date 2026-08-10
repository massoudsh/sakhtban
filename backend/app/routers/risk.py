"""روتر Risk Heatmap — تجمیع سه لایه (issue #4, #19, #25)."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.deviation import RiskItem
from app.schemas.deviation import RiskItemOut

router = APIRouter(prefix="/risk-heatmap", tags=["risk-heatmap"])


@router.get("/{project_id}", response_model=list[RiskItemOut])
def get_heatmap(project_id: uuid.UUID, include_resolved: bool = False, db: Session = Depends(get_db)) -> list[RiskItem]:
    """داده‌ی خام heatmap: هر RiskItem مستقل از این‌که از کدام لایه (زمان‌بندی/تصمیم/QA) آمده،
    با severity_score و likelihood_score قابل‌رسم روی یک شبکه‌ی واحد است.
    """
    stmt = select(RiskItem).where(RiskItem.project_id == project_id)
    if not include_resolved:
        stmt = stmt.where(RiskItem.is_resolved.is_(False))
    return list(db.scalars(stmt))


@router.post("/{risk_item_id}/resolve", response_model=RiskItemOut)
def resolve_risk_item(risk_item_id: uuid.UUID, db: Session = Depends(get_db)) -> RiskItem:
    item = db.get(RiskItem, risk_item_id)
    item.is_resolved = True
    db.commit()
    db.refresh(item)
    return item
