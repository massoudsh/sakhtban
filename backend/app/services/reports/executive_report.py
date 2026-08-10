"""گزارش‌گیری اجرایی برای کارفرما و سرمایه‌گذار (issue #14)."""
from datetime import date

from app.models.deviation import ActionItem, Deviation, RiskItem
from app.services.reports.report_builder import ExecutiveReport, ReportSection


def build_executive_report(
    project_id: str,
    top_risks: list[RiskItem],
    open_deviations: list[Deviation],
    open_action_items: list[ActionItem],
    as_of: date,
) -> ExecutiveReport:
    """خلاصه‌ی سطح‌بالا برای کارفرما/سرمایه‌گذار: مهم‌ترین ریسک‌ها، انحراف‌های باز و اقدام‌های در جریان."""
    risk_section = ReportSection(
        title="مهم‌ترین ریسک‌های باز پروژه",
        summary=f"{len(top_risks)} ریسک باز در Risk Heatmap شناسایی شده است.",
        items=[
            {
                "title": r.title,
                "location": r.location,
                "severity_score": float(r.severity_score),
                "likelihood_score": float(r.likelihood_score),
                "source_type": r.source_type.value,
            }
            for r in top_risks
        ],
    )

    deviation_section = ReportSection(
        title="انحراف‌های باز زمان‌بندی/هزینه",
        summary=f"{len(open_deviations)} انحراف هنوز رفع نشده است.",
        items=[
            {
                "type": d.deviation_type.value,
                "severity": d.severity.value,
                "variance_days": d.variance_days,
                "description": d.description,
            }
            for d in open_deviations
        ],
    )

    action_section = ReportSection(
        title="اقدام‌های در جریان",
        summary=f"{len(open_action_items)} action item باز یا در حال انجام است.",
        items=[{"title": a.title, "status": a.status.value, "due_date": a.due_date} for a in open_action_items],
    )

    return ExecutiveReport(
        report_type="executive_summary",
        project_id=project_id,
        generated_at=as_of,
        title="گزارش اجرایی وضعیت پروژه",
        sections=[risk_section, deviation_section, action_section],
    )
