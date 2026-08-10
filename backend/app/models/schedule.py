"""مدل برنامه‌ی زمان‌بندی، baseline و import (issue #9, #10, #13)."""
import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class ScheduleSource(str, enum.Enum):
    PRIMAVERA_XER = "primavera_xer"
    MS_PROJECT = "ms_project"
    MANUAL = "manual"


class ScheduleImport(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """یک رویداد import برنامه‌ی زمان‌بندی (issue #9)."""

    __tablename__ = "schedule_imports"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    source: Mapped[ScheduleSource] = mapped_column(Enum(ScheduleSource))
    original_filename: Mapped[str] = mapped_column(String(500))
    is_baseline: Mapped[bool] = mapped_column(default=False)

    tasks: Mapped[list["ScheduleTask"]] = relationship(back_populates="schedule_import", cascade="all, delete-orphan")


class TaskStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ScheduleTask(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """یک فعالیت در برنامه‌ی زمان‌بندی. baseline_* از نسخه‌ی مبنا و actual_* از واقعیت اجرا پر می‌شود."""

    __tablename__ = "schedule_tasks"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    schedule_import_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schedule_imports.id", ondelete="CASCADE"))

    external_task_id: Mapped[str] = mapped_column(String(100))  # task_id در XER / UID در MSPDI
    name: Mapped[str] = mapped_column(String(500))
    wbs_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    baseline_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    baseline_finish: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_finish: Mapped[date | None] = mapped_column(Date, nullable=True)
    forecast_finish: Mapped[date | None] = mapped_column(Date, nullable=True)

    percent_complete: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED)

    schedule_import: Mapped["ScheduleImport"] = relationship(back_populates="tasks")
    predecessors: Mapped[list["TaskDependency"]] = relationship(
        foreign_keys="TaskDependency.successor_id", back_populates="successor", cascade="all, delete-orphan"
    )


class TaskDependency(UUIDPrimaryKeyMixin, Base):
    """وابستگی بین فعالیت‌ها، پایه‌ی موتور پیش‌بینی اثر زنجیره‌ای تأخیر (issue #13)."""

    __tablename__ = "task_dependencies"

    predecessor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schedule_tasks.id", ondelete="CASCADE"))
    successor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schedule_tasks.id", ondelete="CASCADE"))
    lag_days: Mapped[int] = mapped_column(default=0)

    successor: Mapped["ScheduleTask"] = relationship(foreign_keys=[successor_id], back_populates="predecessors")
