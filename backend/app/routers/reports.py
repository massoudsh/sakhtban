"""روتر گزارش کارگاه — دریافت از وب و تلگرام، پارس NLP (issue #1, #2, #6)."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.report import ReportChannel, ReportEntity, ReportStatus, SiteReport
from app.schemas.report import SiteReportCreate, SiteReportOut, TelegramWebhookPayload
from app.services.nlp_parser import extract_entities

router = APIRouter(prefix="/reports", tags=["reports"])


def _parse_and_persist(report: SiteReport, db: Session) -> None:
    parsed = extract_entities(report.raw_text)
    for entity in parsed.entities:
        db.add(
            ReportEntity(
                report_id=report.id,
                entity_type=entity.entity_type,
                value=entity.value,
                quantity=entity.quantity,
                unit=entity.unit,
                confidence=entity.confidence,
            )
        )
    report.status = ReportStatus.PARSED
    db.commit()
    db.refresh(report)


@router.post("", response_model=SiteReportOut, status_code=status.HTTP_201_CREATED)
def submit_report(payload: SiteReportCreate, db: Session = Depends(get_db)) -> SiteReport:
    """ثبت گزارش از فرم وب (issue #6 — کانال web)."""
    report = SiteReport(
        project_id=payload.project_id,
        channel=payload.channel,
        raw_text=payload.raw_text,
        report_date=payload.report_date,
    )
    db.add(report)
    db.flush()
    _parse_and_persist(report, db)
    return report


@router.get("/{report_id}", response_model=SiteReportOut)
def get_report(report_id: uuid.UUID, db: Session = Depends(get_db)) -> SiteReport:
    report = db.get(SiteReport, report_id)
    if not report:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "گزارش پیدا نشد.")
    return report


@router.post("/telegram-webhook", status_code=status.HTTP_200_OK)
def telegram_webhook(payload: TelegramWebhookPayload, db: Session = Depends(get_db)) -> dict:
    """دریافت گزارش هفتگی از ربات تلگرام (issue #6 — کانال telegram).

    نکته: نگاشت chat_id تلگرام به project_id باید در جدول جداگانه‌ی project_telegram_binding
    نگه‌داشته شود (خارج از scope این اسکلت اولیه)؛ اینجا برای سادگی از یک متادیتای ثابت
    در payload استفاده می‌شود.
    """
    message = payload.message
    text = message.get("text", "")
    project_id = message.get("project_id")  # در پیاده‌سازی نهایی از bind chat<->project خوانده می‌شود
    if not project_id or not text:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "پیام تلگرام فاقد متن یا شناسه‌ی پروژه است.")

    report = SiteReport(
        project_id=uuid.UUID(project_id),
        channel=ReportChannel.TELEGRAM,
        raw_text=text,
        report_date=message.get("date", ""),
    )
    db.add(report)
    db.flush()
    _parse_and_persist(report, db)
    return {"ok": True, "report_id": str(report.id)}
