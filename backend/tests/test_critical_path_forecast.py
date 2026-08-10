from datetime import date
import uuid

from app.models.schedule import ScheduleTask, TaskDependency
from app.services.critical_path_forecast import forecast_delay_impact


def test_delay_propagates_to_successor():
    task_a_id = uuid.uuid4()
    task_b_id = uuid.uuid4()

    task_a = ScheduleTask(id=task_a_id, name="فعالیت الف", baseline_finish=date(2026, 1, 10))
    task_b = ScheduleTask(id=task_b_id, name="فعالیت ب", baseline_finish=date(2026, 1, 15))

    dependency = TaskDependency(predecessor_id=task_a_id, successor_id=task_b_id, lag_days=0)

    impacts = forecast_delay_impact(
        tasks=[task_a, task_b],
        dependencies=[dependency],
        source_task_id=str(task_a_id),
        delay_days=7,
    )

    assert len(impacts) == 1
    assert impacts[0].task_id == str(task_b_id)
    assert impacts[0].delay_days == 7
    assert impacts[0].new_forecast_finish == date(2026, 1, 22)
