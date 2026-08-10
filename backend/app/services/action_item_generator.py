"""تولید خودکار Action Item از انحراف تشخیص‌داده‌شده (issue #5)."""
from app.models.deviation import ActionItem, ActionItemStatus, Deviation, DeviationSeverity

# فقط انحراف‌های medium به بالا action item می‌سازند تا صندوق ورودی مدیر پروژه شلوغ نشود
_SEVERITY_THRESHOLD = {DeviationSeverity.MEDIUM, DeviationSeverity.HIGH, DeviationSeverity.CRITICAL}

_TEMPLATES = {
    DeviationSeverity.MEDIUM: "بررسی و برنامه‌ریزی جبران عقب‌افتادگی",
    DeviationSeverity.HIGH: "تصمیم فوری برای جبران تأخیر یا اصلاح برنامه لازم است",
    DeviationSeverity.CRITICAL: "این انحراف می‌تواند مسیر بحرانی را تحت تأثیر قرار دهد — تصمیم امروز لازم است",
}


def build_action_item_for_deviation(deviation: Deviation) -> ActionItem | None:
    """اگر انحراف به‌اندازه‌ی کافی جدی بود، یک ActionItem پیش‌نویس برمی‌گرداند (هنوز به DB اضافه نشده)."""
    if deviation.severity not in _SEVERITY_THRESHOLD:
        return None

    title = f"{_TEMPLATES[deviation.severity]}: {deviation.description[:80]}"
    return ActionItem(
        project_id=deviation.project_id,
        deviation_id=deviation.id,
        title=title,
        description=deviation.description,
        status=ActionItemStatus.OPEN,
    )
