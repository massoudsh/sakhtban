"""موتور تشخیص ابهام و ریسک اختلاف روی تصمیم‌های ثبت‌شده (issue #17).

قوانین صریح و قابل‌توضیح — چون خروجی این موتور مستقیماً وارد Risk Heatmap می‌شود
و مدیر پروژه باید بتواند به کارفرما/پیمانکار توضیح دهد چرا یک تصمیم «پرریسک» علامت خورده.
"""
from dataclasses import dataclass

from app.models.decision import AmbiguityType, Decision, DecisionStatus

# کلمات نشان‌دهنده‌ی تناقض وقتی در کنار تصمیم‌های مشابه دیده شوند (چک ساده‌ی متنی، نه semantic)
_CONTRADICTION_HINTS = ["برخلاف", "بر خلاف", "در تناقض با", "لغو نامه‌ی قبلی"]


@dataclass
class DetectedAmbiguity:
    ambiguity_type: AmbiguityType
    explanation: str
    risk_score: float


def evaluate_decision(decision: Decision, related_decisions: list[Decision] | None = None) -> list[DetectedAmbiguity]:
    """یک تصمیم را بر اساس چهار قانون ساده ارزیابی می‌کند و صفر یا چند پرچم ابهام برمی‌گرداند."""
    flags: list[DetectedAmbiguity] = []

    if decision.status in (DecisionStatus.PARTIALLY_APPROVED, DecisionStatus.UNCLEAR):
        flags.append(
            DetectedAmbiguity(
                ambiguity_type=AmbiguityType.INCOMPLETE_APPROVAL,
                explanation=f"تصمیم «{decision.statement[:100]}» تأیید کامل ندارد (وضعیت: {decision.status.value}).",
                risk_score=65.0,
            )
        )

    if decision.financial_impact is None and any(
        kw in decision.statement for kw in ["تغییر", "اضافه‌کار", "متمم", "افزایش", "کاهش"]
    ):
        flags.append(
            DetectedAmbiguity(
                ambiguity_type=AmbiguityType.MISSING_FINANCIAL_IMPACT,
                explanation="این تصمیم به‌نظر تغییر در محدوده/هزینه دارد اما اثر مالی آن ثبت نشده است.",
                risk_score=70.0,
            )
        )

    if not decision.responsible_party:
        flags.append(
            DetectedAmbiguity(
                ambiguity_type=AmbiguityType.MISSING_RESPONSIBLE_PARTY,
                explanation="مسئول پیگیری/اجرای این تصمیم در سند مشخص نشده است.",
                risk_score=45.0,
            )
        )

    if any(hint in decision.statement for hint in _CONTRADICTION_HINTS):
        flags.append(
            DetectedAmbiguity(
                ambiguity_type=AmbiguityType.CONTRADICTION,
                explanation="این تصمیم به‌صراحت با سند/تصمیم دیگری در تناقض است.",
                risk_score=85.0,
            )
        )

    return flags
