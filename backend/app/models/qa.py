"""مدل داده‌ی QA Copilot — لایه‌ی سوم (issue #21, #22, #23, #24, #25)."""
import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class DefectSeverity(str, enum.Enum):
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"


class DefectStatus(str, enum.Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    FIXED = "fixed"          # پیمانکار اصلاح را اعلام کرده
    VERIFIED = "verified"    # ناظر تأیید کرده (عکس بعد از اصلاح تطبیق دارد)
    REOPENED = "reopened"    # اصلاح رد شده، دوباره باز شده -> نشانه‌ی rework


class Defect(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """یک ایراد کیفی ثبت‌شده از اپ موبایل: عکس + موقعیت + توضیح (issue #21, #22)."""

    __tablename__ = "defects"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    reported_by_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    contractor_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)  # مثل «برق»، «نازک‌کاری»، «سازه»
    location: Mapped[str] = mapped_column(String(255))  # طبقه/زون/اتاق
    photo_before_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    photo_after_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    gps_lat: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    gps_lng: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)

    severity: Mapped[DefectSeverity] = mapped_column(Enum(DefectSeverity), default=DefectSeverity.MINOR)
    status: Mapped[DefectStatus] = mapped_column(Enum(DefectStatus), default=DefectStatus.OPEN)
    reopened_count: Mapped[int] = mapped_column(default=0)  # شمارنده‌ی rework برای این ایراد

    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    punch_item: Mapped["PunchItem | None"] = relationship(back_populates="defect", uselist=False)


class PunchItemStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class PunchItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """آیتم punch list خودکار تولیدشده از Defect برای پیگیری اصلاح (issue #23)."""

    __tablename__ = "punch_items"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    defect_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("defects.id", ondelete="CASCADE"), unique=True)
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    status: Mapped[PunchItemStatus] = mapped_column(Enum(PunchItemStatus), default=PunchItemStatus.OPEN)
    closed_at: Mapped[date | None] = mapped_column(Date, nullable=True)

    defect: Mapped["Defect"] = relationship(back_populates="punch_item")


class ReworkPattern(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """الگوی تکرار ایراد/rework محاسبه‌شده روی یک بازه — منبع RiskItem از نوع qa_rework_pattern (issue #24, #25)."""

    __tablename__ = "rework_patterns"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))

    dimension: Mapped[str] = mapped_column(String(50))   # "contractor" | "location" | "category"
    dimension_value: Mapped[str] = mapped_column(String(255))  # مثلاً نام پیمانکار یا «طبقه ۳»
    defect_count: Mapped[int] = mapped_column()
    reopened_count: Mapped[int] = mapped_column()
    rework_rate: Mapped[float] = mapped_column(Numeric(5, 2))  # reopened_count / defect_count * 100
    period_start: Mapped[date] = mapped_column(Date)
    period_end: Mapped[date] = mapped_column(Date)
