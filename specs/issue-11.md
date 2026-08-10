# Issue #11 — ماژول ثبت و رهگیری هزینه‌ی پروژه

> فاز ۲ — هزینه و خرید · [GitHub Issue #11](https://github.com/massoudsh/sakhtban/issues/11)

## مسئله

هزینه‌ی واقعی باید به‌تفکیک دسته و در مقایسه با بودجه‌ی مصوب رهگیری شود.

## طرح فنی

`Budget` ردیف بودجه‌ی مصوب و `CostEntry` هزینه‌ی واقعی را نگه می‌دارد. اندپوینت `/costs/{project_id}/variance` مجموع هزینه‌ی هر بودجه را با `approved_amount` مقایسه و درصد انحراف را برمی‌گرداند — ورودی مستقیم به Risk Heatmap در فازهای بعد (RiskSourceType.COST_DEVIATION از قبل در مدل تعریف شده).

## فایل‌های کد مرتبط

- `backend/app/models/cost.py`
- `backend/app/routers/cost.py`

## وضعیت

کامل.

## معیار پذیرش

- [x] ثبت CostEntry و محاسبه‌ی درست variance_percent نسبت به بودجه.
