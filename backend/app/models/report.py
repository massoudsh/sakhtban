"""مدل داده‌ی گزارش‌های کارگاه و موجودیت‌های استخراج‌شده (issue #1, #2, #6)."""
import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class ReportChannel(str, enum.Enum):
    WEB = "web"
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"


class ReportStatus(str, enum.Enum):
    RECEIVED = "received"
    PARSED = "parsed"
    NEEDS_REVIEW = "needs_review"
    PROCESSED = "processed"


class SiteReport(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """گزارش خام روزانه/هفتگی کارگاه — ورودی خام برای پارسر NLP (issue #2)."""

    __tablename__ = "site_reports"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    submitted_by_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    channel: Mapped[ReportChannel] = mapped_column(Enum(ReportChannel), default=ReportChannel.WEB)
    raw_text: Mapped[str] = mapped_column(Text)
    report_date: Mapped[str] = mapped_column(String(10))  # YYYY-MM-DD (تقویم شمسی یا میلادی نگاشت‌شده)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), default=ReportStatus.RECEIVED)

    entities: Mapped[list["ReportEntity"]] = relationship(back_populates="report", cascade="all, delete-orphan")


class ReportEntityType(str, enum.Enum):
    ACTIVITY = "activity"       # فعالیت اجرایی (مثل «بتن‌ریزی سقف طبقه ۳»)
    QUANTITY = "quantity"       # مقدار انجام‌شده
    LOCATION = "location"       # موقعیت/طبقه/بلوک
    DELAY_REASON = "delay_reason"  # علت تأخیر ذکرشده در متن آزاد
    RESOURCE = "resource"       # نیروی انسانی / ماشین‌آلات / پیمانکار


class ReportEntity(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """موجودیت ساخت‌یافته‌ی استخراج‌شده از متن آزاد گزارش، خروجی پارسر NLP فارسی."""

    __tablename__ = "report_entities"

    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("site_reports.id", ondelete="CASCADE"))

    entity_type: Mapped[ReportEntityType] = mapped_column(Enum(ReportEntityType))
    value: Mapped[str] = mapped_column(String(500))
    quantity: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    confidence: Mapped[float] = mapped_column(default=0.5)  # اطمینان استخراج (۰ تا ۱)

    report: Mapped["SiteReport"] = relationship(back_populates="entities")
