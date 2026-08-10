"""پارسر خروجی MS Project به فرمت MSPDI XML (issue #9).

توضیح تصمیم فنی: فایل باینری .mpp نیازمند کتابخانه‌های سنگین (مثل MPXJ روی JVM) است.
در MVP از کاربر خواسته می‌شود پروژه را به فرمت XML استاندارد «Microsoft Project XML
(MSPDI)» اکسپورت کند (File > Save As > XML در MS Project) که یک فرمت باز و مستند است.
اگر بعداً نیاز به .mpp مستقیم بود، این ماژول با یک microservice مبتنی بر MPXJ جایگزین می‌شود
بدون تغییر در contract (خروجی همیشه XerTask-like/ScheduleTask records است).
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from xml.etree import ElementTree as ET

_NS = {"ns": "http://schemas.microsoft.com/project"}


def _parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


@dataclass
class MspTask:
    uid: str
    name: str
    start: date | None
    finish: date | None
    actual_start: date | None
    actual_finish: date | None
    percent_complete: float


@dataclass
class MspPredecessorLink:
    task_uid: str
    predecessor_uid: str
    lag_days: int


@dataclass
class MspParseResult:
    tasks: list[MspTask] = field(default_factory=list)
    predecessors: list[MspPredecessorLink] = field(default_factory=list)


def _text(el: ET.Element | None) -> str | None:
    return el.text if el is not None else None


def parse_mspdi_xml(content: bytes | str) -> MspParseResult:
    root = ET.fromstring(content)
    result = MspParseResult()

    for task_el in root.findall("ns:Tasks/ns:Task", _NS):
        uid = _text(task_el.find("ns:UID", _NS)) or ""
        if uid == "0":
            continue  # UID=0 خلاصه‌ی کل پروژه است، نه یک فعالیت واقعی

        result.tasks.append(
            MspTask(
                uid=uid,
                name=_text(task_el.find("ns:Name", _NS)) or "",
                start=_parse_iso_date(_text(task_el.find("ns:Start", _NS))),
                finish=_parse_iso_date(_text(task_el.find("ns:Finish", _NS))),
                actual_start=_parse_iso_date(_text(task_el.find("ns:ActualStart", _NS))),
                actual_finish=_parse_iso_date(_text(task_el.find("ns:ActualFinish", _NS))),
                percent_complete=float(_text(task_el.find("ns:PercentComplete", _NS)) or 0),
            )
        )

        for link_el in task_el.findall("ns:PredecessorLink", _NS):
            pred_uid = _text(link_el.find("ns:PredecessorUID", _NS))
            lag_str = _text(link_el.find("ns:LinkLag", _NS)) or "0"
            lag_format = _text(link_el.find("ns:LagFormat", _NS)) or "7"  # 7 = روز
            lag_days = int(lag_str) if lag_format in ("7", "8") else 0
            if pred_uid:
                result.predecessors.append(
                    MspPredecessorLink(task_uid=uid, predecessor_uid=pred_uid, lag_days=lag_days)
                )

    return result
