# Issue #19 — اتصال Decision Log به Risk Heatmap موجود

> فاز ۴ — Decision Log و پیشگیری از اختلاف · [GitHub Issue #19](https://github.com/massoudsh/sakhtban/issues/19)

## مسئله

ابهام تصمیم باید همان جایی دیده شود که انحراف زمان‌بندی/هزینه دیده می‌شود، نه در یک ابزار جدا.

## طرح فنی

`risk_item_from_ambiguity` هر `AmbiguityFlag` را به یک `RiskItem` با `source_type=DECISION_AMBIGUITY` تبدیل می‌کند. این تبدیل مستقیماً داخل `POST /decisions/documents` (لحظه‌ی آپلود سند) اتفاق می‌افتد — بدون نیاز به یک job جدا.

## فایل‌های کد مرتبط

- `backend/app/services/risk_heatmap.py (risk_item_from_ambiguity)`
- `backend/app/routers/decisions.py (upload_document)`

## وضعیت

کامل.

## معیار پذیرش

- [x] آپلود سند با تصمیم مبهم، بلافاصله یک RiskItem جدید در heatmap تولید کند.
