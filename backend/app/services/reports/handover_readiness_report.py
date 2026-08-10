"""گزارش آمادگی تحویل (Handover Readiness Report) — issue #26.

خروجی لایه‌ی QA Copilot: قبل از تحویل واحد/طبقه/پروژه، وضعیت باز بودن ایرادها و
الگوی rework را یک‌جا نشان می‌دهد تا معلوم شود آیا واقعاً آماده‌ی تحویل هست یا نه.
"""
from datetime import date

from app.models.qa import Defect
from app.services.reports.report_builder import ExecutiveReport, ReportSection
from app.services.rework_pattern_engine import ReworkPatternResult


def build_handover_readiness_report(
    project_id: str,
    open_defects: list[Defect],
    rework_patterns: list[ReworkPatternResult],
    as_of: date,
    scope_label: str,
) -> ExecutiveReport:
    critical_open = [d for d in open_defects if d.severity.value == "critical"]

    defect_section = ReportSection(
        title=f"ایرادهای باز — {scope_label}",
        summary=(
            f"{len(open_defects)} ایراد باز، از جمله {len(critical_open)} ایراد بحرانی. "
            + ("آماده‌ی تحویل نیست." if critical_open else "ایراد بحرانی باز وجود ندارد.")
        ),
        items=[
            {
                "title": d.title,
                "location": d.location,
                "severity": d.severity.value,
                "status": d.status.value,
                "contractor_name": d.contractor_name,
                "reopened_count": d.reopened_count,
            }
            for d in open_defects
        ],
    )

    alert_patterns = [p for p in rework_patterns if p.is_alert]
    rework_section = ReportSection(
        title="الگوهای تکرار ایراد/rework",
        summary=f"{len(alert_patterns)} الگوی rework بالای آستانه‌ی هشدار شناسایی شده است.",
        items=[
            {
                "dimension": p.dimension,
                "dimension_value": p.dimension_value,
                "defect_count": p.defect_count,
                "rework_rate": p.rework_rate,
            }
            for p in alert_patterns
        ],
    )

    return ExecutiveReport(
        report_type="handover_readiness",
        project_id=project_id,
        generated_at=as_of,
        title=f"گزارش آمادگی تحویل — {scope_label}",
        sections=[defect_section, rework_section],
    )
