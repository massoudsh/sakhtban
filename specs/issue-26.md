# Issue #26 — گزارش آمادگی تحویل (Handover Readiness Report)

> فاز ۵ — QA Copilot و کنترل کیفیت اجرا · [GitHub Issue #26](https://github.com/massoudsh/sakhtban/issues/26)

## مسئله

قبل از تحویل واحد/طبقه/پروژه باید مشخص شود آیا واقعاً از نظر کیفیت آماده است یا نه.

## طرح فنی

`build_handover_readiness_report` ایرادهای باز (با تأکید بر بحرانی‌ها) و الگوهای rework بالای آستانه را برای یک scope مشخص (مثلاً «طبقه ۳» یا «کل پروژه») جمع می‌کند و یک جمع‌بندی صریح («آماده‌ی تحویل نیست» / «ایراد بحرانی باز وجود ندارد») تولید می‌کند.

## فایل‌های کد مرتبط

- `backend/app/services/reports/handover_readiness_report.py`
- `backend/app/routers/qa.py (handover_readiness_report)`

## وضعیت

کامل.

## معیار پذیرش

- [x] وجود حتی یک ایراد critical باز، پیام «آماده‌ی تحویل نیست» تولید کند.
