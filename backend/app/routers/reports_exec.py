"""روتر گزارش‌گیری اجرایی برای کارفرما و سرمایه‌گذار (issue #14)."""
import uuid
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.deviation import ActionItem, ActionItemStatus, Deviation, RiskItem
from app.services.reports.executive_report import build_executive_report

router = APIRouter(prefix="/executive-report", tags=["executive-report"])


@router.get("/{project_id}")
def get_executive_report(project_id: uuid.UUID, top_n_risks: int = 10, db: Session = Depends(get_db)) -> dict:
    top_risks = list(
        db.scalars(
            select(RiskItem)
            .where(RiskItem.project_id == project_id, RiskItem.is_resolved.is_(False))
            .order_by(RiskItem.severity_score.desc())
            .limit(top_n_risks)
        )
    )
    open_deviations = list(db.scalars(select(Deviation).where(Deviation.project_id == project_id)))
    open_action_items = list(
        db.scalars(
            select(ActionItem).where(
                ActionItem.project_id == project_id, ActionItem.status != ActionItemStatus.DONE
            )
        )
    )

    report = build_executive_report(
        project_id=str(project_id),
        top_risks=top_risks,
        open_deviations=open_deviations,
        open_action_items=open_action_items,
        as_of=date.today(),
    )
    return report.to_dict()
