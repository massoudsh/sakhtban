"""روتر برنامه‌ی زمان‌بندی — import و موتور تطبیق (issue #9, #10)."""
import uuid
from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.schedule import ScheduleImport, ScheduleSource, ScheduleTask, TaskDependency, TaskStatus
from app.schemas.schedule import ScheduleTaskOut
from app.services.deviation_engine import detect_schedule_deviations
from app.services.risk_heatmap import risk_item_from_deviation
from app.services.schedule_import.msproject_parser import parse_mspdi_xml
from app.services.schedule_import.xer_parser import parse_xer

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("/{project_id}/import/xer", status_code=status.HTTP_201_CREATED)
async def import_xer(
    project_id: uuid.UUID,
    is_baseline: bool = False,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    content = (await file.read()).decode("utf-8", errors="ignore")
    parsed = parse_xer(content)

    schedule_import = ScheduleImport(
        project_id=project_id,
        source=ScheduleSource.PRIMAVERA_XER,
        original_filename=file.filename or "import.xer",
        is_baseline=is_baseline,
    )
    db.add(schedule_import)
    db.flush()

    task_id_map: dict[str, uuid.UUID] = {}
    for xer_task in parsed.tasks:
        task = ScheduleTask(
            project_id=project_id,
            schedule_import_id=schedule_import.id,
            external_task_id=xer_task.task_id,
            name=xer_task.task_name,
            baseline_start=xer_task.target_start if is_baseline else None,
            baseline_finish=xer_task.target_end if is_baseline else None,
            actual_start=xer_task.act_start,
            actual_finish=xer_task.act_end,
            percent_complete=xer_task.percent_complete,
            status=TaskStatus.COMPLETED if xer_task.act_end else TaskStatus.IN_PROGRESS,
        )
        db.add(task)
        db.flush()
        task_id_map[xer_task.task_id] = task.id

    for pred in parsed.predecessors:
        if pred.task_id in task_id_map and pred.pred_task_id in task_id_map:
            db.add(
                TaskDependency(
                    predecessor_id=task_id_map[pred.pred_task_id],
                    successor_id=task_id_map[pred.task_id],
                    lag_days=pred.lag_days,
                )
            )

    db.commit()
    return {"schedule_import_id": str(schedule_import.id), "task_count": len(parsed.tasks)}


@router.post("/{project_id}/import/msproject-xml", status_code=status.HTTP_201_CREATED)
async def import_msproject_xml(
    project_id: uuid.UUID,
    is_baseline: bool = False,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    content = await file.read()
    parsed = parse_mspdi_xml(content)

    schedule_import = ScheduleImport(
        project_id=project_id,
        source=ScheduleSource.MS_PROJECT,
        original_filename=file.filename or "import.xml",
        is_baseline=is_baseline,
    )
    db.add(schedule_import)
    db.flush()

    uid_map: dict[str, uuid.UUID] = {}
    for msp_task in parsed.tasks:
        task = ScheduleTask(
            project_id=project_id,
            schedule_import_id=schedule_import.id,
            external_task_id=msp_task.uid,
            name=msp_task.name,
            baseline_start=msp_task.start if is_baseline else None,
            baseline_finish=msp_task.finish if is_baseline else None,
            actual_start=msp_task.actual_start,
            actual_finish=msp_task.actual_finish,
            percent_complete=msp_task.percent_complete,
            status=TaskStatus.COMPLETED if msp_task.actual_finish else TaskStatus.IN_PROGRESS,
        )
        db.add(task)
        db.flush()
        uid_map[msp_task.uid] = task.id

    for link in parsed.predecessors:
        if link.task_uid in uid_map and link.predecessor_uid in uid_map:
            db.add(
                TaskDependency(
                    predecessor_id=uid_map[link.predecessor_uid],
                    successor_id=uid_map[link.task_uid],
                    lag_days=link.lag_days,
                )
            )

    db.commit()
    return {"schedule_import_id": str(schedule_import.id), "task_count": len(parsed.tasks)}


@router.get("/{project_id}/tasks", response_model=list[ScheduleTaskOut])
def list_tasks(project_id: uuid.UUID, db: Session = Depends(get_db)) -> list[ScheduleTask]:
    stmt = select(ScheduleTask).where(ScheduleTask.project_id == project_id)
    return list(db.scalars(stmt))


@router.post("/{project_id}/detect-deviations")
def run_deviation_detection(project_id: uuid.UUID, db: Session = Depends(get_db)) -> dict:
    """اجرای موتور تشخیص انحراف (issue #3) روی همه‌ی فعالیت‌های پروژه."""
    from app.models.deviation import Deviation, DeviationSeverity

    tasks = list(db.scalars(select(ScheduleTask).where(ScheduleTask.project_id == project_id)))
    if not tasks:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "فعالیتی برای این پروژه یافت نشد.")

    # فقط انحراف‌های medium به بالا وارد Risk Heatmap می‌شوند تا با آستانه‌ی
    # تولید Action Item (issue #5) و بقیه‌ی منابع ریسک (issue #19, #25) همسان بماند.
    risk_worthy = {DeviationSeverity.MEDIUM, DeviationSeverity.HIGH, DeviationSeverity.CRITICAL}

    detected = detect_schedule_deviations(tasks, as_of=date.today())
    created = []
    risk_items_created = 0
    for d in detected:
        deviation = Deviation(
            project_id=project_id,
            schedule_task_id=uuid.UUID(d.schedule_task_id),
            deviation_type=d.deviation_type,
            severity=d.severity,
            variance_days=d.variance_days,
            description=d.description,
        )
        db.add(deviation)
        db.flush()
        created.append(deviation)

        if deviation.severity in risk_worthy:
            db.add(risk_item_from_deviation(deviation))
            risk_items_created += 1

    db.commit()
    return {"deviations_created": len(created), "risk_items_created": risk_items_created}
