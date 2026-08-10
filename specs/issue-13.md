# Issue #13 — پیش‌بینی اثر زنجیره‌ای تأخیر (critical path impact forecasting)

> فاز ۳ — لایه‌ی Execution Intelligence · [GitHub Issue #13](https://github.com/massoudsh/sakhtban/issues/13)

## مسئله

مدیر پروژه باید بداند اگر یک فعالیت امروز دیر شود، چه فعالیت‌های دیگری زنجیره‌وار عقب می‌افتند.

## طرح فنی

`forecast_delay_impact` یک forward-pass BFS روی گراف `TaskDependency` است (نه CPM کامل با float مثبت/منفی — هدف MVP سرعت و شفافیت است، نه دقت مهندسی کامل). تأخیر از فعالیت مبدأ به همه‌ی جانشین‌های زنجیره‌ای پخش می‌شود، با کم‌کردن lag موجود در هر وابستگی.

## فایل‌های کد مرتبط

- `backend/app/services/critical_path_forecast.py`
- `backend/app/routers/forecast.py`
- `backend/tests/test_critical_path_forecast.py`

## وضعیت

کامل و تست‌شده برای حالت پایه (finish-to-start).

## معیار پذیرش

- [x] تأخیر یک فعالیت مبدأ به‌درستی به جانشین مستقیم آن با کم‌کردن lag منتقل شود.
