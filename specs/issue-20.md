# Issue #20 — گزارش آمادگی مذاکره/داوری (Dispute-Readiness Report)

> فاز ۴ — Decision Log و پیشگیری از اختلاف · [GitHub Issue #20](https://github.com/massoudsh/sakhtban/issues/20)

## مسئله

قبل از جلسه‌ی مذاکره یا داوری، مدیر پروژه به یک خلاصه از همه‌ی تصمیم‌های پرریسک نیاز دارد.

## طرح فنی

`build_dispute_readiness_report` همه‌ی تصمیم‌هایی که حداقل یک `AmbiguityFlag` دارند را با متن کامل تصمیم، مسئول، اثر مالی و توضیح هر ابهام جمع می‌کند.

## فایل‌های کد مرتبط

- `backend/app/services/reports/dispute_readiness_report.py`
- `backend/app/routers/decisions.py (dispute_readiness_report)`

## وضعیت

کامل.

## معیار پذیرش

- [x] اگر تصمیم پرریسکی وجود نداشته باشد، خطای ۴۰۴ معنادار برگردانده شود.
