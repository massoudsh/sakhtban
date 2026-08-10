from datetime import date

from app.models.deviation import DeviationSeverity
from app.models.schedule import ScheduleTask, TaskStatus
from app.services.deviation_engine import classify_severity, detect_schedule_deviation


def test_classify_severity_thresholds():
    assert classify_severity(1) == DeviationSeverity.LOW
    assert classify_severity(4) == DeviationSeverity.MEDIUM
    assert classify_severity(8) == DeviationSeverity.HIGH
    assert classify_severity(20) == DeviationSeverity.CRITICAL


def test_detect_schedule_deviation_with_actual_finish():
    task = ScheduleTask(
        name="بتن‌ریزی سقف طبقه ۳",
        baseline_finish=date(2026, 1, 10),
        actual_finish=date(2026, 1, 22),
        status=TaskStatus.COMPLETED,
    )
    deviation = detect_schedule_deviation(task, as_of=date(2026, 1, 25))
    assert deviation is not None
    assert deviation.variance_days == 12
    assert deviation.severity == DeviationSeverity.CRITICAL


def test_no_deviation_when_on_time():
    task = ScheduleTask(
        name="نازک‌کاری طبقه ۲",
        baseline_finish=date(2026, 2, 1),
        actual_finish=date(2026, 1, 30),
        status=TaskStatus.COMPLETED,
    )
    assert detect_schedule_deviation(task, as_of=date(2026, 2, 5)) is None
