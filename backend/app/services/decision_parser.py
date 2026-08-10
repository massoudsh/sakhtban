"""پارسر استخراج تصمیم از اسناد پروژه — صورت‌جلسه و نامه (issue #16).

مثل nlp_parser.py، این هم یک heuristic مبتنی بر regex/کلیدواژه است، نه ML.
اسناد صورت‌جلسه و مکاتبات فارسی معمولاً ساختار نیمه‌ثابتی دارند («مقرر شد که...»،
«تصمیم گرفته شد...») که این الگوها را قابل‌اتکا می‌کند.
"""
import re
from dataclasses import dataclass, field

DECISION_MARKERS = [
    r"مقرر\s+(?:شد|گردید)\s+که",
    r"تصمیم\s+(?:گرفته\s+شد|شد)\s*(?:که)?",
    r"تأیید\s+(?:شد|گردید)",
    r"تصویب\s+(?:شد|گردید)",
]

RESPONSIBLE_PATTERN = re.compile(
    r"(?:توسط|مسئولیت با|پیگیری توسط)\s+(?P<name>[\u0600-\u06FF\s]{2,40}?)(?:\s+انجام|\s+صورت|$|،|\.)"
)

AMOUNT_PATTERN = re.compile(r"(?P<amount>[\d,]+)\s*(?:ریال|تومان)")

_DECISION_REGEX = re.compile("|".join(DECISION_MARKERS))


@dataclass
class ExtractedDecision:
    statement: str
    responsible_party: str | None = None
    financial_impact: float | None = None


@dataclass
class ParsedDocument:
    decisions: list[ExtractedDecision] = field(default_factory=list)


def extract_decisions(raw_text: str) -> ParsedDocument:
    """جملاتی که حاوی نشانگر تصمیم‌گیری هستند را به‌عنوان تصمیم استخراج می‌کند."""
    parsed = ParsedDocument()
    sentences = [s.strip() for s in re.split(r"[\n\.؛]+", raw_text) if s.strip()]

    for sentence in sentences:
        if not _DECISION_REGEX.search(sentence):
            continue

        responsible_match = RESPONSIBLE_PATTERN.search(sentence)
        amount_match = AMOUNT_PATTERN.search(sentence)

        parsed.decisions.append(
            ExtractedDecision(
                statement=sentence,
                responsible_party=responsible_match.group("name").strip() if responsible_match else None,
                financial_impact=(
                    float(amount_match.group("amount").replace(",", "")) if amount_match else None
                ),
            )
        )

    return parsed
