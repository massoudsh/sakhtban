"""مدل ثبت لید پایلوت از لندینگ‌پیج (issue #8)."""
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class PilotLead(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """درخواست پایلوت ثبت‌شده از فرم لندینگ‌پیج (docs/index.html)."""

    __tablename__ = "pilot_leads"

    company_name: Mapped[str] = mapped_column(String(255))
    contact_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_contacted: Mapped[bool] = mapped_column(default=False)
