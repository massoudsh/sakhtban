"""مدل انحراف، ریسک و action item (issue #3, #4, #5)."""
import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class DeviationSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DeviationType(str, enum.Enum):
    SCHEDULE = "schedule"
    COST = "cost"
    QUALITY = "quality"       # از QA Copilot (issue #25)
    DECISION = "decision"     # از Decision Log / ابهام (issue #19)


class Deviation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """یک انحراف تشخیص‌داده‌شده توسط موتور rule-based (issue #3)."""

    __tablename__ = "deviations"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    schedule_task_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("schedule_tasks.id", ondelete="SET NULL"), nullable=True
    )

    deviation_type: Mapped[DeviationType] = mapped_column(Enum(DeviationType))
    severity: Mapped[DeviationSeverity] = mapped_column(Enum(DeviationSeverity))
    variance_days: Mapped[int | None] = mapped_column(nullable=True)
    variance_percent: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)
    description: Mapped[str] = mapped_column(Text)

    action_items: Mapped[list["ActionItem"]] = relationship(back_populates="deviation")


class ActionItemStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    IGNORED = "ignored"


class ActionItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """اقدام پیشنهادی خودکار تولیدشده از یک انحراف (issue #5)."""

    __tablename__ = "action_items"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    deviation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("deviations.id"), nullable=True)
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[ActionItemStatus] = mapped_column(Enum(ActionItemStatus), default=ActionItemStatus.OPEN)
    due_date: Mapped[str | None] = mapped_column(String(10), nullable=True)

    deviation: Mapped["Deviation"] = relationship(back_populates="action_items")


class RiskSourceType(str, enum.Enum):
    SCHEDULE_DEVIATION = "schedule_deviation"
    COST_DEVIATION = "cost_deviation"
    DECISION_AMBIGUITY = "decision_ambiguity"   # لایه‌ی دوم (Decision Log)
    QA_REWORK_PATTERN = "qa_rework_pattern"     # لایه‌ی سوم (QA Copilot)


class RiskItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """موجودیت یکپارچه‌ی Risk Heatmap — نقطه‌ی اتصال هر سه لایه (issue #4, #19, #25)."""

    __tablename__ = "risk_items"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))

    source_type: Mapped[RiskSourceType] = mapped_column(Enum(RiskSourceType))
    source_id: Mapped[uuid.UUID] = mapped_column()  # id رکورد مبدأ (Deviation / AmbiguityFlag / ReworkPattern)

    title: Mapped[str] = mapped_column(String(500))
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)  # طبقه/بلوک/زون
    severity_score: Mapped[float] = mapped_column(Numeric(5, 2))  # ۰ تا ۱۰۰، محور رنگ heatmap
    likelihood_score: Mapped[float] = mapped_column(Numeric(5, 2))  # ۰ تا ۱۰۰، محور دیگر heatmap
    is_resolved: Mapped[bool] = mapped_column(default=False)
