"""پارسر NLP فارسی برای گزارش‌های آزاد کارگاه (issue #2).

نسخه‌ی MVP: heuristic مبتنی بر regex و لیست کلیدواژه — بدون وابستگی به مدل ML سنگین،
تا بدون زیرساخت GPU/دیتاست آموزشی هم قابل اجرا باشد. طراحی به‌گونه‌ای است که بعداً
می‌توان extract_entities را با یک مدل NER فارسی (مثل hazm/spaCy) جایگزین کرد بدون
تغییر contract تابع.
"""
import re
from dataclasses import dataclass, field

from app.models.report import ReportEntityType

# کلیدواژه‌های علت تأخیر رایج در گزارش‌های کارگاهی فارسی
DELAY_KEYWORDS = [
    "تأخیر", "تاخیر", "کمبود", "نبود", "خرابی", "توقف", "قطعی برق",
    "بارش باران", "بارندگی", "کمبود نیرو", "کمبود مصالح", "دیرکرد",
    "مشکل تأمین", "عدم دسترسی", "تعطیلی",
]

# واحدهای متریک رایج در گزارش ساختمانی
UNIT_PATTERN = r"(متر مربع|متر مکعب|مترمربع|مترمکعب|کیلوگرم|تن|عدد|متر طول|مترطول|m2|m3|kg)"

QUANTITY_PATTERN = re.compile(
    rf"(?P<qty>\d+(?:[.,]\d+)?)\s*(?P<unit>{UNIT_PATTERN})", re.IGNORECASE
)

# موقعیت‌های رایج: طبقه/بلوک/زون + شماره (فارسی یا لاتین)
LOCATION_PATTERN = re.compile(
    r"(طبقه|بلوک|زون|واحد|قطعه)\s*(?P<num>[\d۰-۹]+)"
)

# نگاشت اعداد فارسی به لاتین برای نرمال‌سازی
_PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


def _normalize_digits(text: str) -> str:
    return text.translate(_PERSIAN_DIGITS)


@dataclass
class ExtractedEntity:
    entity_type: ReportEntityType
    value: str
    quantity: float | None = None
    unit: str | None = None
    confidence: float = 0.5


@dataclass
class ParsedReport:
    entities: list[ExtractedEntity] = field(default_factory=list)


def _split_sentences(text: str) -> list[str]:
    # جدا کردن جملات با نقطه، خط جدید یا نقطه‌ویرگول — متن گزارش‌های کارگاهی معمولاً کوتاه و تلگرافی است
    parts = re.split(r"[\n\.؛;]+", text)
    return [p.strip() for p in parts if p.strip()]


def extract_entities(raw_text: str) -> ParsedReport:
    """استخراج فعالیت، مقدار، موقعیت و علت تأخیر از متن آزاد یک گزارش کارگاه."""
    text = _normalize_digits(raw_text)
    parsed = ParsedReport()

    for sentence in _split_sentences(text):
        found_something = False

        for match in LOCATION_PATTERN.finditer(sentence):
            parsed.entities.append(
                ExtractedEntity(
                    entity_type=ReportEntityType.LOCATION,
                    value=f"{match.group(1)} {match.group('num')}",
                    confidence=0.8,
                )
            )
            found_something = True

        qty_match = QUANTITY_PATTERN.search(sentence)
        if qty_match:
            qty_value = float(qty_match.group("qty").replace(",", "."))
            parsed.entities.append(
                ExtractedEntity(
                    entity_type=ReportEntityType.QUANTITY,
                    value=sentence,
                    quantity=qty_value,
                    unit=qty_match.group("unit"),
                    confidence=0.7,
                )
            )
            found_something = True

        delay_hit = next((kw for kw in DELAY_KEYWORDS if kw in sentence), None)
        if delay_hit:
            parsed.entities.append(
                ExtractedEntity(
                    entity_type=ReportEntityType.DELAY_REASON,
                    value=sentence,
                    confidence=0.6,
                )
            )
            found_something = True

        # اگر هیچ‌کدام از الگوهای بالا نبود ولی جمله طولانی‌تر از چند کلمه بود،
        # به‌عنوان توصیف فعالیت با اطمینان پایین‌تر ثبت می‌شود تا چیزی از دست نرود.
        if not found_something and len(sentence.split()) >= 3:
            parsed.entities.append(
                ExtractedEntity(
                    entity_type=ReportEntityType.ACTIVITY,
                    value=sentence,
                    confidence=0.4,
                )
            )

    return parsed
