"""روتر Decision Log — پارس سند، ابهام، خط زمانی، اتصال به heatmap (issue #15-#20)."""
import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.decision import AmbiguityFlag, Decision, DecisionDocument, DecisionStatus
from app.schemas.decision import DecisionDocumentCreate, DecisionDocumentOut, DecisionOut
from app.services.decision_parser import extract_decisions
from app.services.dispute_risk_engine import evaluate_decision
from app.services.reports.dispute_readiness_report import build_dispute_readiness_report
from app.services.risk_heatmap import risk_item_from_ambiguity

router = APIRouter(prefix="/decisions", tags=["decisions"])


@router.post("/documents", response_model=DecisionDocumentOut, status_code=status.HTTP_201_CREATED)
def upload_document(payload: DecisionDocumentCreate, db: Session = Depends(get_db)) -> DecisionDocument:
    """آپلود سند (صورت‌جلسه/نامه) + پارس خودکار تصمیم‌ها (issue #16) + تشخیص ابهام (issue #17)
    + اتصال به Risk Heatmap (issue #19)."""
    document = DecisionDocument(**payload.model_dump())
    db.add(document)
    db.flush()

    parsed = extract_decisions(document.raw_text)
    for extracted in parsed.decisions:
        decision = Decision(
            project_id=document.project_id,
            document_id=document.id,
            responsible_party=extracted.responsible_party,
            statement=extracted.statement,
            decision_date=document.document_date,
            status=DecisionStatus.APPROVED if extracted.responsible_party else DecisionStatus.UNCLEAR,
            financial_impact=extracted.financial_impact,
        )
        db.add(decision)
        db.flush()

        ambiguities = evaluate_decision(decision)
        for amb in ambiguities:
            flag = AmbiguityFlag(
                decision_id=decision.id,
                ambiguity_type=amb.ambiguity_type,
                explanation=amb.explanation,
                risk_score=amb.risk_score,
            )
            db.add(flag)
            db.flush()
            db.add(risk_item_from_ambiguity(flag, decision))

    db.commit()
    db.refresh(document)
    return document


@router.get("/{project_id}/timeline", response_model=list[DecisionOut])
def decision_timeline(project_id: uuid.UUID, db: Session = Depends(get_db)) -> list[Decision]:
    """خط زمانی تصمیم‌ها، مرتب بر اساس تاریخ (issue #18)."""
    stmt = (
        select(Decision)
        .where(Decision.project_id == project_id)
        .order_by(Decision.decision_date.asc().nulls_last())
    )
    return list(db.scalars(stmt))


@router.get("/{project_id}/dispute-readiness-report")
def dispute_readiness_report(project_id: uuid.UUID, db: Session = Depends(get_db)) -> dict:
    """گزارش آمادگی مذاکره/داوری (issue #20)."""
    stmt = select(Decision).where(Decision.project_id == project_id)
    decisions = list(db.scalars(stmt))
    flagged = [(d, d.ambiguity_flags) for d in decisions if d.ambiguity_flags]

    if not flagged:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "هیچ تصمیم پرریسکی برای این پروژه یافت نشد.")

    report = build_dispute_readiness_report(project_id=str(project_id), flagged_decisions=flagged, as_of=date.today())
    return report.to_dict()
