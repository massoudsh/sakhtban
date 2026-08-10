# Issue #5 — تولید خودکار Action Item از انحراف

> فاز ۰ — Wedge MVP · [GitHub Issue #5](https://github.com/massoudsh/sakhtban/issues/5)

## مسئله

تشخیص انحراف به‌تنهایی کافی نیست — باید یک اقدام مشخص و قابل‌پیگیری تولید شود.

## طرح فنی

`build_action_item_for_deviation` فقط برای انحراف‌های medium به بالا action item می‌سازد (تا صندوق ورودی شلوغ نشود) و بر اساس severity از یک تمپلیت عنوان مناسب استفاده می‌کند. اندپوینت `/deviations/{id}/generate-action-item` این تابع را صدا می‌زند و رکورد را ذخیره می‌کند.

## فایل‌های کد مرتبط

- `backend/app/services/action_item_generator.py`
- `backend/app/routers/deviations.py`

## وضعیت

کامل.

## معیار پذیرش

- [x] انحراف low هیچ action item ای تولید نکند.
- [x] action item تولیدشده به deviation مبدأ لینک باشد.
