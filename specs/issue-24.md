# Issue #24 — تشخیص الگوی تکرار ایراد و rework (پیمانکار/طبقه/دسته)

> فاز ۵ — QA Copilot و کنترل کیفیت اجرا · [GitHub Issue #24](https://github.com/massoudsh/sakhtban/issues/24)

## مسئله

مدیر پروژه باید بداند کدام پیمانکار/طبقه/دسته بیشترین rework را دارد، نه فقط تعداد خام ایراد.

## طرح فنی

`compute_rework_patterns` ایرادها را بر اساس یک بُعد (contractor/location/category) گروه‌بندی و `rework_rate = reopened/defect_count*100` را حساب می‌کند. زیر آستانه‌ی حداقل نمونه (۳ ایراد) یا نرخ rework (۲۰٪) الگو alert نمی‌شود تا نویز آماری حذف شود.

## فایل‌های کد مرتبط

- `backend/app/services/rework_pattern_engine.py`
- `backend/tests/test_rework_pattern_engine.py`

## وضعیت

کامل و تست‌شده.

## معیار پذیرش

- [x] گروهی با نمونه‌ی کم یا rework_rate پایین، is_alert=False داشته باشد.
