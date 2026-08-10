"""مدل هزینه و خرید پروژه (issue #11, #12)."""
import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class CostCategory(str, enum.Enum):
    MATERIAL = "material"
    LABOR = "labor"
    EQUIPMENT = "equipment"
    SUBCONTRACTOR = "subcontractor"
    OVERHEAD = "overhead"


class Budget(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """بودجه‌ی مصوب هر ردیف هزینه (خط مبنای مقایسه برای انحراف هزینه)."""

    __tablename__ = "budgets"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    category: Mapped[CostCategory] = mapped_column(Enum(CostCategory))
    wbs_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    approved_amount: Mapped[float] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(10), default="IRR")

    entries: Mapped[list["CostEntry"]] = relationship(back_populates="budget")


class CostEntry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """رکورد هزینه‌ی واقعی ثبت‌شده (issue #11)."""

    __tablename__ = "cost_entries"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    budget_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("budgets.id"), nullable=True)

    category: Mapped[CostCategory] = mapped_column(Enum(CostCategory))
    description: Mapped[str] = mapped_column(Text)
    amount: Mapped[float] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(10), default="IRR")
    entry_date: Mapped[date] = mapped_column(Date)

    budget: Mapped["Budget"] = relationship(back_populates="entries")


class ProcurementStatus(str, enum.Enum):
    REQUESTED = "requested"
    ORDERED = "ordered"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    DELAYED = "delayed"


class ProcurementItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """قلم خرید/تأمین با رهگیری وضعیت (issue #12)."""

    __tablename__ = "procurement_items"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    schedule_task_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("schedule_tasks.id", ondelete="SET NULL"), nullable=True
    )

    item_name: Mapped[str] = mapped_column(String(500))
    supplier: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity: Mapped[float] = mapped_column(Numeric(12, 2))
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[ProcurementStatus] = mapped_column(Enum(ProcurementStatus), default=ProcurementStatus.REQUESTED)

    expected_delivery: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_delivery: Mapped[date | None] = mapped_column(Date, nullable=True)
