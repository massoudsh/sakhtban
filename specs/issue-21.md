# Issue #21 — طراحی مدل داده QA (Defect / Punch Item)

> فاز ۵ — QA Copilot و کنترل کیفیت اجرا · [GitHub Issue #21](https://github.com/massoudsh/sakhtban/issues/21)

## مسئله

ایرادهای کیفی باید با عکس، موقعیت، شدت و وضعیت پیگیری ساخت‌یافته ذخیره شوند.

## طرح فنی

`Defect` عکس قبل/بعد، GPS، شدت (minor/major/critical) و `reopened_count` (شمارنده‌ی rework) را نگه می‌دارد. `PunchItem` به‌صورت خودکار از هر Defect ساخته می‌شود و وضعیت پیگیری اصلاح را جدا مدیریت می‌کند.

## فایل‌های کد مرتبط

- `backend/app/models/qa.py`

## وضعیت

کامل.

## معیار پذیرش

- [x] هر Defect حداکثر یک PunchItem مرتبط داشته باشد (unique constraint روی defect_id).
