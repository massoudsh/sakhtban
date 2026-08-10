"""پیش‌بینی اثر زنجیره‌ای تأخیر روی فعالیت‌های وابسته (issue #13).

نسخه‌ی MVP یک forward-pass ساده روی گراف وابستگی‌هاست (نه CPM کامل با float منفی/مثبت):
اگر فعالیت A دیر تمام شود، همه‌ی جانشین‌هایش (successors) که finish-to-start وابسته‌اند
به همان اندازه (منهای هر float موجود) عقب می‌افتند، به‌صورت زنجیره‌ای تا انتهای شبکه.
هدف: به مدیر پروژه نشان دهد «اگر همین امروز تصمیم نگیری، سه هفته‌ی دیگر این فعالیت‌ها
هم دیر می‌شوند» — نه محاسبه‌ی دقیق مهندسی CPM.
"""
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import date, timedelta

from app.models.schedule import ScheduleTask, TaskDependency


@dataclass
class ForecastImpact:
    task_id: str
    task_name: str
    delay_days: int
    new_forecast_finish: date


def forecast_delay_impact(
    tasks: list[ScheduleTask],
    dependencies: list[TaskDependency],
    source_task_id: str,
    delay_days: int,
) -> list[ForecastImpact]:
    """اثر تأخیر یک فعالیت مشخص را روی همه‌ی جانشین‌های زنجیره‌ای آن محاسبه می‌کند."""
    tasks_by_id = {str(t.id): t for t in tasks}
    successors_map: dict[str, list[TaskDependency]] = defaultdict(list)
    for dep in dependencies:
        successors_map[str(dep.predecessor_id)].append(dep)

    if source_task_id not in tasks_by_id:
        return []

    impacts: dict[str, ForecastImpact] = {}
    queue: deque[tuple[str, int]] = deque([(source_task_id, delay_days)])
    visited_delay: dict[str, int] = {source_task_id: delay_days}

    while queue:
        current_id, current_delay = queue.popleft()

        for dep in successors_map.get(current_id, []):
            successor_id = str(dep.successor_id)
            successor = tasks_by_id.get(successor_id)
            if successor is None:
                continue

            # تأخیر اثرگذار روی جانشین = تأخیر فعلی منهای lag موجود در وابستگی (اگر lag منفی جذب کند)
            propagated_delay = max(0, current_delay - dep.lag_days)
            if propagated_delay <= 0:
                continue

            already = visited_delay.get(successor_id, 0)
            if propagated_delay <= already:
                continue  # این مسیر تأخیر بیشتری اضافه نمی‌کند

            visited_delay[successor_id] = propagated_delay
            base_finish = successor.baseline_finish or successor.forecast_finish
            if base_finish is None:
                continue

            new_finish = base_finish + timedelta(days=propagated_delay)
            impacts[successor_id] = ForecastImpact(
                task_id=successor_id,
                task_name=successor.name,
                delay_days=propagated_delay,
                new_forecast_finish=new_finish,
            )
            queue.append((successor_id, propagated_delay))

    return sorted(impacts.values(), key=lambda i: i.new_forecast_finish)
