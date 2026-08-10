from app.services.schedule_import.msproject_parser import parse_mspdi_xml

_SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Project xmlns="http://schemas.microsoft.com/project">
  <Tasks>
    <Task>
      <UID>0</UID>
      <Name>پروژه</Name>
    </Task>
    <Task>
      <UID>1</UID>
      <Name>فعالیت اول</Name>
      <Start>2026-01-01T08:00:00</Start>
      <Finish>2026-01-10T17:00:00</Finish>
      <PercentComplete>100</PercentComplete>
      <ActualStart>2026-01-01T08:00:00</ActualStart>
      <ActualFinish>2026-01-12T17:00:00</ActualFinish>
    </Task>
    <Task>
      <UID>2</UID>
      <Name>فعالیت دوم</Name>
      <Start>2026-01-11T08:00:00</Start>
      <Finish>2026-01-20T17:00:00</Finish>
      <PercentComplete>0</PercentComplete>
      <PredecessorLink>
        <PredecessorUID>1</PredecessorUID>
        <LinkLag>0</LinkLag>
        <LagFormat>7</LagFormat>
      </PredecessorLink>
    </Task>
  </Tasks>
</Project>
"""


def test_parses_tasks_skipping_project_summary_and_reads_predecessors():
    result = parse_mspdi_xml(_SAMPLE_XML)
    assert len(result.tasks) == 2  # UID=0 (خلاصه‌ی پروژه) نباید شمرده شود
    assert result.tasks[0].name == "فعالیت اول"
    assert result.tasks[0].actual_finish is not None

    assert len(result.predecessors) == 1
    assert result.predecessors[0].task_uid == "2"
    assert result.predecessors[0].predecessor_uid == "1"
