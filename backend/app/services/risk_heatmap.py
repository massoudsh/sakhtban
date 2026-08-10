"""تجمیع سه منبع ریسک (زمان‌بندی/هزینه، ابهام تصمیم، الگوی rework) در یک Risk Heatmap واحد.

این ماژول نقطه‌ی اتصال هر سه لایه‌ی محصول است:
- لایه‌ی اول: Deviation (schedule/cost) -> issue #4
- لایه‌ی دوم: AmbiguityFlag (Decision Log) -> issue #19
- لایه‌ی سوم: ReworkPattern (QA Copilot) -> issue #25

خروجی یک لیست از RiskItem با severity_score/likelihood_score قابل‌مقایسه است
تا UI بتواند همه را روی یک heatmap واحد نشان دهد، نه سه ابزار جدا.
"""
from app.models.decision import AmbiguityFlag, Decision
from app.models.deviation import Deviation, DeviationSeverity, RiskItem, RiskSourceType
from app.models.qa import ReworkPattern

_SEVERITY_TO_SCORE = {
    DeviationSeverity.LOW: 25.0,
    DeviationSeverity.MEDIUM: 50.0,
    DeviationSeverity.HIGH: 75.0,
    DeviationSeverity.CRITICAL: 95.0,
}


def risk_item_from_deviation(deviation: Deviation) -> RiskItem:
    return RiskItem(
        project_id=deviation.project_id,
        source_type=RiskSourceType.SCHEDULE_DEVIATION,
        source_id=deviation.id,
        title=deviation.description[:200],
        severity_score=_SEVERITY_TO_SCORE[deviation.severity],
        likelihood_score=min(100.0, (deviation.variance_days or 0) * 5),
    )


def risk_item_from_ambiguity(flag: AmbiguityFlag, decision: Decision) -> RiskItem:
    return RiskItem(
        project_id=decision.project_id,
        source_type=RiskSourceType.DECISION_AMBIGUITY,
        source_id=flag.id,
        title=f"ابهام تصمیم: {flag.explanation[:180]}",
        severity_score=float(flag.risk_score),
        # تصمیم‌های بدون اثر مالی ثبت‌شده احتمال بیشتری دارد در آینده به اختلاف تبدیل شوند
        likelihood_score=70.0 if decision.financial_impact is None else 40.0,
    )


def risk_item_from_rework_pattern(pattern: ReworkPattern) -> RiskItem:
    return RiskItem(
        project_id=pattern.project_id,
        source_type=RiskSourceType.QA_REWORK_PATTERN,
        source_id=pattern.id,
        title=f"تکرار ایراد در {pattern.dimension_value} ({pattern.dimension})",
        location=pattern.dimension_value if pattern.dimension == "location" else None,
        severity_score=min(100.0, float(pattern.rework_rate)),
        likelihood_score=min(100.0, pattern.defect_count * 4.0),
    )
