"""ساختار مشترک گزارش‌های اجرایی (issue #14, #20, #26).

خروجی این ماژول یک payload ساخت‌یافته‌ی JSON است، نه PDF — رندر نهایی (PDF/چاپ)
در لایه‌ی جدا (مثلاً با noqte-render سمت پنل) انجام می‌شود تا این سرویس بدون
وابستگی به موتور رندر سنگین باقی بماند.
"""
from dataclasses import dataclass, field
from datetime import date


@dataclass
class ReportSection:
    title: str
    items: list[dict] = field(default_factory=list)
    summary: str | None = None


@dataclass
class ExecutiveReport:
    report_type: str
    project_id: str
    generated_at: date
    title: str
    sections: list[ReportSection] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "report_type": self.report_type,
            "project_id": self.project_id,
            "generated_at": self.generated_at.isoformat(),
            "title": self.title,
            "sections": [
                {"title": s.title, "summary": s.summary, "items": s.items} for s in self.sections
            ],
        }
