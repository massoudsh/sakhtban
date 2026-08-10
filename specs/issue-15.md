# Issue #15 — طراحی مدل داده Decision Log

> فاز ۴ — Decision Log و پیشگیری از اختلاف · [GitHub Issue #15](https://github.com/massoudsh/sakhtban/issues/15)

## مسئله

تصمیم‌های پروژه (صورت‌جلسه/نامه) باید ساخت‌یافته با مسئول، تاریخ، وضعیت تأیید و اثر مالی ذخیره شوند.

## طرح فنی

`DecisionDocument` سند خام را نگه می‌دارد؛ `Decision` هر تصمیم استخراج‌شده را با `responsible_party`، `status` (proposed/approved/partially_approved/rejected/unclear) و `financial_impact` نگه می‌دارد؛ `AmbiguityFlag` پرچم ریسک روی هر تصمیم است.

## فایل‌های کد مرتبط

- `backend/app/models/decision.py`

## وضعیت

کامل.

## معیار پذیرش

- [x] هر Decision قابل اتصال به یک DecisionDocument و صفر یا چند AmbiguityFlag باشد.
