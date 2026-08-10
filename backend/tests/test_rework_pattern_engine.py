from datetime import date

from app.models.qa import Defect
from app.services.rework_pattern_engine import compute_rework_patterns


def _defect(contractor: str, reopened: int = 0) -> Defect:
    return Defect(
        title="ایراد نمونه",
        description="توضیح",
        location="طبقه ۱",
        contractor_name=contractor,
        reopened_count=reopened,
    )


def test_alert_triggered_for_high_rework_rate():
    defects = [
        _defect("پیمانکار الف", reopened=1),
        _defect("پیمانکار الف", reopened=1),
        _defect("پیمانکار الف", reopened=0),
        _defect("پیمانکار ب", reopened=0),
    ]
    results = compute_rework_patterns(defects, dimension="contractor", period_start=date(2026, 1, 1), period_end=date(2026, 3, 1))
    by_contractor = {r.dimension_value: r for r in results}

    assert by_contractor["پیمانکار الف"].defect_count == 3
    assert by_contractor["پیمانکار الف"].rework_rate > 20
    assert by_contractor["پیمانکار الف"].is_alert is True
    assert by_contractor["پیمانکار ب"].is_alert is False
