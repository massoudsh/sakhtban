"""پارسر فایل Primavera XER (issue #9).

فرمت XER یک فایل متنی tab-delimited است: هر جدول با `%T <table_name>` شروع می‌شود،
سطر بعد `%F` نام ستون‌هاست و سطرهای بعدی `%R` داده هستند. اینجا فقط دو جدول موردنیاز
برای Sakhtban را می‌خوانیم: TASK (فعالیت‌ها) و TASKPRED (وابستگی‌ها).
"""
from dataclasses import dataclass, field
from datetime import date, datetime


def _parse_xer_date(value: str) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


@dataclass
class XerTask:
    task_id: str
    task_code: str
    task_name: str
    target_start: date | None
    target_end: date | None
    act_start: date | None
    act_end: date | None
    percent_complete: float


@dataclass
class XerTaskPred:
    task_id: str
    pred_task_id: str
    lag_days: int


@dataclass
class XerParseResult:
    tasks: list[XerTask] = field(default_factory=list)
    predecessors: list[XerTaskPred] = field(default_factory=list)


def _parse_table(lines: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    columns = lines[0].rstrip("\n").split("\t")[1:]  # حذف مارکر %F
    rows = []
    for line in lines[1:]:
        if not line.startswith("%R"):
            break
        values = line.rstrip("\n").split("\t")[1:]
        rows.append(dict(zip(columns, values)))
    return columns, rows


def parse_xer(content: str) -> XerParseResult:
    lines = content.splitlines(keepends=True)
    result = XerParseResult()

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("%T\t"):
            table_name = line.strip().split("\t")[1]
            # جدول از خط بعد (%F) شروع می‌شود؛ سطرها تا برخورد با %T بعدی یا %E ادامه دارند
            block = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith("%T"):
                if lines[j].startswith("%E"):
                    j += 1
                    break
                block.append(lines[j])
                j += 1

            if block and table_name == "TASK":
                _columns, rows = _parse_table(block)
                for row in rows:
                    result.tasks.append(
                        XerTask(
                            task_id=row.get("task_id", ""),
                            task_code=row.get("task_code", ""),
                            task_name=row.get("task_name", ""),
                            target_start=_parse_xer_date(row.get("target_start_date", "")),
                            target_end=_parse_xer_date(row.get("target_end_date", "")),
                            act_start=_parse_xer_date(row.get("act_start_date", "")),
                            act_end=_parse_xer_date(row.get("act_end_date", "")),
                            percent_complete=float(row.get("phys_complete_pct") or 0),
                        )
                    )
            elif block and table_name == "TASKPRED":
                _columns, rows = _parse_table(block)
                for row in rows:
                    lag_hours = float(row.get("lag_hr_cnt") or 0)
                    result.predecessors.append(
                        XerTaskPred(
                            task_id=row.get("task_id", ""),
                            pred_task_id=row.get("pred_task_id", ""),
                            lag_days=int(lag_hours / 8),  # فرض ۸ ساعت کاری در روز
                        )
                    )
            i = j
        else:
            i += 1

    return result
