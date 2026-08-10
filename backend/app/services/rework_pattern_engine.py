"""تشخیص الگوی تکرار ایراد و rework بر اساس پیمانکار/طبقه/دسته (issue #24).

منطق: روی یک بازه‌ی زمانی، ایرادها را بر اساس هر بُعد (پیمانکار/موقعیت/دسته) گروه‌بندی
می‌کند و rework_rate را به‌صورت (تعداد بازگشایی‌شده / کل ایرادها) محاسبه می‌کند.
هر گروهی که از حد آستانه بگذرد، الگوی rework محسوب می‌شود و به Risk Heatmap متصل می‌شود
(از طریق risk_heatmap.risk_item_from_rework_pattern).
"""
from collections import defaultdict
from dataclasses import dataclass
from datetime import date

from app.models.qa import Defect

_MIN_DEFECT_COUNT_FOR_PATTERN = 3  # زیر این تعداد، نمونه برای نتیجه‌گیری آماری کافی نیست
_REWORK_RATE_ALERT_THRESHOLD = 20.0  # درصد


@dataclass
class ReworkPatternResult:
    dimension: str
    dimension_value: str
    defect_count: int
    reopened_count: int
    rework_rate: float
    is_alert: bool


def _dimension_value(defect: Defect, dimension: str) -> str | None:
    if dimension == "contractor":
        return defect.contractor_name
    if dimension == "location":
        return defect.location
    if dimension == "category":
        return defect.category
    raise ValueError(f"بُعد ناشناخته: {dimension}")


def compute_rework_patterns(
    defects: list[Defect], dimension: str, period_start: date, period_end: date
) -> list[ReworkPatternResult]:
    grouped: dict[str, list[Defect]] = defaultdict(list)
    for defect in defects:
        value = _dimension_value(defect, dimension)
        if value:
            grouped[value].append(defect)

    results = []
    for value, group in grouped.items():
        defect_count = len(group)
        reopened_count = sum(d.reopened_count for d in group)
        rework_rate = round((reopened_count / defect_count) * 100, 2) if defect_count else 0.0

        results.append(
            ReworkPatternResult(
                dimension=dimension,
                dimension_value=value,
                defect_count=defect_count,
                reopened_count=reopened_count,
                rework_rate=rework_rate,
                is_alert=(
                    defect_count >= _MIN_DEFECT_COUNT_FOR_PATTERN
                    and rework_rate >= _REWORK_RATE_ALERT_THRESHOLD
                ),
            )
        )

    return sorted(results, key=lambda r: r.rework_rate, reverse=True)
