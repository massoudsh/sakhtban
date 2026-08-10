"""موتور تشخیص انحراف baseline-vs-actual (issue #3).

قوانین ساده و شفاف (rule-based)، نه ML جعبه‌سیاه — چون مدیر پروژه باید بتواند
بفهمد «چرا این هشدار صادر شد». آستانه‌ها قابل‌تنظیم برای هر پروژه هستند.
"""
from dataclasses import dataclass
from datetime import date

from app.models.deviation import DeviationSeverity, DeviationType
from app.models.schedule import ScheduleTask


@dataclass
class DeviationThresholds:
    low_days: int = 2
    medium_days: int = 5
    high_days: int = 10
    # critical: بیشتر از high_days


def classify_severity(variance_days: int, thresholds: DeviationThresholds = DeviationThresholds()) -> DeviationSeverity:
    magnitude = abs(variance_days)
    if magnitude <= thresholds.low_days:
        return DeviationSeverity.LOW
    if magnitude <= thresholds.medium_days:
        return DeviationSeverity.MEDIUM
    if magnitude <= thresholds.high_days:
        return DeviationSeverity.HIGH
    return DeviationSeverity.CRITICAL


@dataclass
class DetectedDeviation:
    schedule_task_id: str
    deviation_type: DeviationType
    variance_days: int
    severity: DeviationSeverity
    description: str


def detect_schedule_deviation(
    task: ScheduleTask, as_of: date, thresholds: DeviationThresholds = DeviationThresholds()
) -> DetectedDeviation | None:
    """مقایسه‌ی baseline_finish با forecast/actual finish یک فعالیت.

    منطق:
    - اگر actual_finish ثبت شده -> واقعیت نهایی را با baseline مقایسه کن.
    - وگرنه اگر forecast_finish هست -> پیش‌بینی را با baseline مقایسه کن.
    - وگرنه اگر فعالیت هنوز تمام نشده و از baseline_finish گذشته‌ایم -> انحراف "در حال وقوع".
    """
    if task.baseline_finish is None:
        return None

    reference_finish = task.actual_finish or task.forecast_finish
    if reference_finish is None:
        if task.status.value != "completed" and as_of > task.baseline_finish:
            reference_finish = as_of
        else:
            return None

    variance_days = (reference_finish - task.baseline_finish).days
    if variance_days <= 0:
        return None  # جلوتر یا هم‌زمان با برنامه — انحراف نیست

    severity = classify_severity(variance_days, thresholds)
    description = (
        f"فعالیت «{task.name}» {variance_days} روز از تاریخ پایان مبنا "
        f"({task.baseline_finish.isoformat()}) عقب‌تر است."
    )
    return DetectedDeviation(
        schedule_task_id=str(task.id),
        deviation_type=DeviationType.SCHEDULE,
        variance_days=variance_days,
        severity=severity,
        description=description,
    )


def detect_schedule_deviations(
    tasks: list[ScheduleTask], as_of: date, thresholds: DeviationThresholds = DeviationThresholds()
) -> list[DetectedDeviation]:
    results = []
    for task in tasks:
        deviation = detect_schedule_deviation(task, as_of, thresholds)
        if deviation:
            results.append(deviation)
    return results
