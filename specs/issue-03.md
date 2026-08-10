# Issue #3 — موتور تشخیص انحراف (baseline rule-based)

> فاز ۰ — Wedge MVP · [GitHub Issue #3](https://github.com/massoudsh/sakhtban/issues/3)

## مسئله

باید عقب‌افتادگی هر فعالیت نسبت به baseline به‌صورت خودکار و قابل‌توضیح (نه جعبه‌سیاه) تشخیص داده شود.

## طرح فنی

`detect_schedule_deviation` تاریخ پایان واقعی/پیش‌بینی/امروز را با `baseline_finish` مقایسه می‌کند و variance_days را با آستانه‌های قابل‌تنظیم (`DeviationThresholds`) به low/medium/high/critical طبقه‌بندی می‌کند. قوانین صریح‌اند تا مدیر پروژه بتواند توضیح هشدار را بفهمد.

## فایل‌های کد مرتبط

- `backend/app/services/deviation_engine.py`
- `backend/app/routers/schedule.py (detect-deviations)`
- `backend/tests/test_deviation_engine.py`

## وضعیت

کامل و تست‌شده.

## معیار پذیرش

- [x] فعالیت جلوتر یا هم‌زمان با برنامه انحراف تولید نکند.
- [x] طبقه‌بندی شدت بر اساس آستانه‌های پیکربندی‌پذیر باشد.
- [x] فعالیت بدون actual/forecast ولی گذشته از baseline نیز به‌عنوان «در حال وقوع» تشخیص داده شود.
