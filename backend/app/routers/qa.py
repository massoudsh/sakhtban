"""روتر QA Copilot — ثبت ایراد، punch list، rework pattern، اتصال به heatmap (issue #21-#26)."""
import uuid
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.qa import Defect, DefectStatus, PunchItem, PunchItemStatus, ReworkPattern
from app.schemas.qa import (
    DefectCreate,
    DefectFixSubmit,
    DefectOut,
    DefectVerify,
    PunchItemOut,
    ReworkPatternOut,
)
from app.services.reports.handover_readiness_report import build_handover_readiness_report
from app.services.risk_heatmap import risk_item_from_rework_pattern
from app.services.rework_pattern_engine import compute_rework_patterns

router = APIRouter(prefix="/qa", tags=["qa"])


@router.post("/defects", response_model=DefectOut, status_code=status.HTTP_201_CREATED)
def report_defect(payload: DefectCreate, db: Session = Depends(get_db)) -> Defect:
    """ثبت ایراد از اپ موبایل (issue #22) + ساخت خودکار punch item (issue #23)."""
    defect = Defect(**payload.model_dump())
    db.add(defect)
    db.flush()

    db.add(PunchItem(project_id=defect.project_id, defect_id=defect.id))
    db.commit()
    db.refresh(defect)
    return defect


@router.get("/{project_id}/defects", response_model=list[DefectOut])
def list_defects(project_id: uuid.UUID, open_only: bool = True, db: Session = Depends(get_db)) -> list[Defect]:
    stmt = select(Defect).where(Defect.project_id == project_id)
    if open_only:
        stmt = stmt.where(Defect.status != DefectStatus.VERIFIED)
    return list(db.scalars(stmt))


@router.post("/defects/{defect_id}/submit-fix", response_model=DefectOut)
def submit_fix(defect_id: uuid.UUID, payload: DefectFixSubmit, db: Session = Depends(get_db)) -> Defect:
    """پیمانکار عکس بعد از اصلاح را ثبت می‌کند (issue #23 پیگیری اصلاح)."""
    defect = db.get(Defect, defect_id)
    if not defect:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "ایراد پیدا نشد.")

    defect.photo_after_url = payload.photo_after_url
    defect.status = DefectStatus.FIXED
    db.commit()
    db.refresh(defect)
    return defect


@router.post("/defects/{defect_id}/verify", response_model=DefectOut)
def verify_fix(defect_id: uuid.UUID, payload: DefectVerify, db: Session = Depends(get_db)) -> Defect:
    """ناظر اصلاح را تأیید یا رد می‌کند. رد شدن = بازگشایی = افزایش شمارنده‌ی rework (issue #23, #24)."""
    defect = db.get(Defect, defect_id)
    if not defect:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "ایراد پیدا نشد.")

    if payload.approved:
        defect.status = DefectStatus.VERIFIED
        punch_item = db.scalar(select(PunchItem).where(PunchItem.defect_id == defect_id))
        if punch_item:
            punch_item.status = PunchItemStatus.CLOSED
            punch_item.closed_at = date.today()
    else:
        defect.status = DefectStatus.REOPENED
        defect.reopened_count += 1

    db.commit()
    db.refresh(defect)
    return defect


@router.get("/{project_id}/punch-list", response_model=list[PunchItemOut])
def punch_list(project_id: uuid.UUID, status_filter: PunchItemStatus | None = None, db: Session = Depends(get_db)) -> list[PunchItem]:
    stmt = select(PunchItem).where(PunchItem.project_id == project_id)
    if status_filter:
        stmt = stmt.where(PunchItem.status == status_filter)
    return list(db.scalars(stmt))


@router.post("/{project_id}/analyze-rework-patterns", response_model=list[ReworkPatternOut])
def analyze_rework_patterns(
    project_id: uuid.UUID,
    dimension: str = "contractor",
    lookback_days: int = 90,
    db: Session = Depends(get_db),
) -> list[ReworkPatternOut]:
    """اجرای موتور تشخیص الگوی تکرار/rework (issue #24) + اتصال نتایج به Risk Heatmap (issue #25)."""
    period_start = date.today() - timedelta(days=lookback_days)
    period_end = date.today()

    stmt = select(Defect).where(Defect.project_id == project_id)
    defects = list(db.scalars(stmt))

    results = compute_rework_patterns(defects, dimension=dimension, period_start=period_start, period_end=period_end)

    for r in results:
        if not r.is_alert:
            continue
        pattern = ReworkPattern(
            project_id=project_id,
            dimension=r.dimension,
            dimension_value=r.dimension_value,
            defect_count=r.defect_count,
            reopened_count=r.reopened_count,
            rework_rate=r.rework_rate,
            period_start=period_start,
            period_end=period_end,
        )
        db.add(pattern)
        db.flush()
        db.add(risk_item_from_rework_pattern(pattern))

    db.commit()
    return [
        ReworkPatternOut(
            dimension=r.dimension,
            dimension_value=r.dimension_value,
            defect_count=r.defect_count,
            reopened_count=r.reopened_count,
            rework_rate=r.rework_rate,
            is_alert=r.is_alert,
        )
        for r in results
    ]


@router.get("/{project_id}/handover-readiness-report")
def handover_readiness_report(project_id: uuid.UUID, scope_label: str = "کل پروژه", db: Session = Depends(get_db)) -> dict:
    """گزارش آمادگی تحویل (issue #26)."""
    open_defects = list(
        db.scalars(
            select(Defect).where(Defect.project_id == project_id, Defect.status != DefectStatus.VERIFIED)
        )
    )
    patterns = list(db.scalars(select(ReworkPattern).where(ReworkPattern.project_id == project_id)))

    from app.services.rework_pattern_engine import ReworkPatternResult

    pattern_results = [
        ReworkPatternResult(
            dimension=p.dimension,
            dimension_value=p.dimension_value,
            defect_count=p.defect_count,
            reopened_count=p.reopened_count,
            rework_rate=float(p.rework_rate),
            is_alert=True,
        )
        for p in patterns
    ]

    report = build_handover_readiness_report(
        project_id=str(project_id),
        open_defects=open_defects,
        rework_patterns=pattern_results,
        as_of=date.today(),
        scope_label=scope_label,
    )
    return report.to_dict()
