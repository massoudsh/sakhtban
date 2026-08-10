from app.services.schedule_import.xer_parser import parse_xer

_SAMPLE_XER = (
    "%T\tTASK\n"
    "%F\ttask_id\ttask_code\ttask_name\ttarget_start_date\ttarget_end_date\tact_start_date\tact_end_date\tphys_complete_pct\n"
    "%R\t1001\tA1000\tبتن‌ریزی فونداسیون\t2026-01-01 08:00\t2026-01-10 17:00\t2026-01-01 08:00\t\t60\n"
    "%R\t1002\tA1010\tاجرای اسکلت\t2026-01-11 08:00\t2026-01-25 17:00\t\t\t0\n"
    "%E\n"
    "%T\tTASKPRED\n"
    "%F\ttask_id\tpred_task_id\tlag_hr_cnt\n"
    "%R\t1002\t1001\t0\n"
    "%E\n"
)


def test_parses_tasks_and_predecessors():
    result = parse_xer(_SAMPLE_XER)
    assert len(result.tasks) == 2
    assert result.tasks[0].task_name == "بتن‌ریزی فونداسیون"
    assert result.tasks[0].act_start is not None
    assert result.tasks[0].act_end is None

    assert len(result.predecessors) == 1
    assert result.predecessors[0].task_id == "1002"
    assert result.predecessors[0].pred_task_id == "1001"
