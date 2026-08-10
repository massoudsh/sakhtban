# Issue #6 — کانال ورود گزارش هفتگی (وب یا تلگرام/واتساپ)

> فاز ۰ — Wedge MVP · [GitHub Issue #6](https://github.com/massoudsh/sakhtban/issues/6)

## مسئله

مدیران کارگاه باید بتوانند گزارش را از همان کانالی که استفاده می‌کنند (وب یا تلگرام) بفرستند.

## طرح فنی

اندپوینت `POST /reports` برای فرم وب و `POST /reports/telegram-webhook` برای ربات تلگرام — هر دو از همان تابع مشترک `_parse_and_persist` برای پارس NLP (issue #2) استفاده می‌کنند. اتصال WhatsApp در MVP اول پیاده نشده (نیاز به WhatsApp Business API که تصمیم تجاری/هزینه‌ای جدا می‌طلبد)؛ ساختار کد اجازه می‌دهد یک `ReportChannel.WHATSAPP` مشابه اضافه شود.

## فایل‌های کد مرتبط

- `backend/app/routers/reports.py`
- `backend/app/models/report.py (ReportChannel)`
- `frontend/src/app/projects/[projectId]/reports/page.tsx`

## وضعیت

کامل برای وب و اسکلت تلگرام؛ WhatsApp نیاز به تصمیم تجاری جدا دارد.

## معیار پذیرش

- [x] گزارش وب مستقیم پارس و ذخیره شود.
- [x] webhook تلگرام پیام را به SiteReport تبدیل کند (نگاشت chat_id→project_id در فاز بعد).
