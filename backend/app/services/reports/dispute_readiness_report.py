"""گزارش آمادگی مذاکره/داوری (Dispute-Readiness Report) — issue #20.

هدف: قبل از جلسه‌ی مذاکره یا داوری، مدیر پروژه یک نگاه واحد از همه‌ی تصمیم‌های
پرریسک/مبهم و مستنداتشان داشته باشد — خروجی مستقیم لایه‌ی Decision Log.
"""
from datetime import date

from app.models.decision import AmbiguityFlag, Decision
from app.services.reports.report_builder import ExecutiveReport, ReportSection


def build_dispute_readiness_report(
    project_id: str,
    flagged_decisions: list[tuple[Decision, list[AmbiguityFlag]]],
    as_of: date,
) -> ExecutiveReport:
    section = ReportSection(
        title="تصمیم‌های پرریسک برای مذاکره/داوری",
        summary=f"{len(flagged_decisions)} تصمیم با حداقل یک پرچم ابهام شناسایی شده است.",
        items=[
            {
                "statement": decision.statement,
                "decision_date": decision.decision_date.isoformat() if decision.decision_date else None,
                "responsible_party": decision.responsible_party,
                "status": decision.status.value,
                "financial_impact": float(decision.financial_impact) if decision.financial_impact else None,
                "ambiguities": [
                    {"type": f.ambiguity_type.value, "explanation": f.explanation, "risk_score": float(f.risk_score)}
                    for f in flags
                ],
            }
            for decision, flags in flagged_decisions
        ],
    )

    return ExecutiveReport(
        report_type="dispute_readiness",
        project_id=project_id,
        generated_at=as_of,
        title="گزارش آمادگی مذاکره/داوری",
        sections=[section],
    )
