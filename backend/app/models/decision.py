"""مدل داده‌ی Decision Log — لایه‌ی دوم (issue #15, #16, #17, #18)."""
import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class DecisionDocumentType(str, enum.Enum):
    MEETING_MINUTES = "meeting_minutes"   # صورت‌جلسه
    LETTER = "letter"                     # نامه‌ی مکاتباتی
    EMAIL = "email"
    OTHER = "other"


class DecisionDocument(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """سند خام پروژه که تصمیم‌ها از آن استخراج می‌شوند (issue #16 پارسر)."""

    __tablename__ = "decision_documents"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    document_type: Mapped[DecisionDocumentType] = mapped_column(Enum(DecisionDocumentType))
    title: Mapped[str] = mapped_column(String(500))
    raw_text: Mapped[str] = mapped_column(Text)
    document_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    decisions: Mapped[list["Decision"]] = relationship(back_populates="document", cascade="all, delete-orphan")


class DecisionStatus(str, enum.Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    PARTIALLY_APPROVED = "partially_approved"
    REJECTED = "rejected"
    UNCLEAR = "unclear"   # تأیید ناقص یا مبهم


class Decision(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """یک تصمیم استخراج‌شده از سند، با مسئول و وضعیت تأیید — هسته‌ی خط زمانی تصمیم‌ها (issue #18)."""

    __tablename__ = "decisions"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    document_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("decision_documents.id"), nullable=True)
    responsible_party: Mapped[str | None] = mapped_column(String(255), nullable=True)

    statement: Mapped[str] = mapped_column(Text)
    decision_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[DecisionStatus] = mapped_column(Enum(DecisionStatus), default=DecisionStatus.PROPOSED)
    financial_impact: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)

    document: Mapped["DecisionDocument"] = relationship(back_populates="decisions")
    ambiguity_flags: Mapped[list["AmbiguityFlag"]] = relationship(back_populates="decision", cascade="all, delete-orphan")


class AmbiguityType(str, enum.Enum):
    INCOMPLETE_APPROVAL = "incomplete_approval"       # تأیید ناقص
    MISSING_FINANCIAL_IMPACT = "missing_financial_impact"  # اثر مالی ثبت‌نشده
    CONTRADICTION = "contradiction"                    # تناقض بین اسناد
    MISSING_RESPONSIBLE_PARTY = "missing_responsible_party"


class AmbiguityFlag(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """ریسک ابهام/اختلاف تشخیص‌داده‌شده روی یک تصمیم — منبع RiskItem از نوع decision_ambiguity (issue #17, #19)."""

    __tablename__ = "ambiguity_flags"

    decision_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("decisions.id", ondelete="CASCADE"))
    ambiguity_type: Mapped[AmbiguityType] = mapped_column(Enum(AmbiguityType))
    explanation: Mapped[str] = mapped_column(Text)
    risk_score: Mapped[float] = mapped_column(Numeric(5, 2))  # ۰ تا ۱۰۰

    decision: Mapped["Decision"] = relationship(back_populates="ambiguity_flags")
