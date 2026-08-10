# Issue #4 — Risk Heatmap — طراحی و پیاده‌سازی UI

> فاز ۰ — Wedge MVP · [GitHub Issue #4](https://github.com/massoudsh/sakhtban/issues/4)

## مسئله

مدیر پروژه باید یک نگاه واحد از همه‌ی ریسک‌های باز پروژه داشته باشد، نه سه ابزار جدا.

## طرح فنی

مدل `RiskItem` نقطه‌ی اتصال هر سه لایه است: `source_type` (schedule_deviation/cost_deviation/decision_ambiguity/qa_rework_pattern) + severity_score/likelihood_score قابل‌مقایسه. اندپوینت `/risk-heatmap/{project_id}` همه‌ی RiskItem های باز پروژه را برمی‌گرداند. صفحه‌ی وب یک لیست رتبه‌بندی‌شده بر اساس severity رسم می‌کند با رنگ متفاوت به‌ازای هر منبع.

## فایل‌های کد مرتبط

- `backend/app/models/deviation.py (RiskItem)`
- `backend/app/routers/risk.py`
- `backend/app/services/risk_heatmap.py`
- `frontend/src/app/projects/[projectId]/risk-heatmap/page.tsx`
- `frontend/src/components/RiskHeatmapGrid.tsx`

## وضعیت

کامل — backend تست‌پذیر، UI اسکلت آماده (نیاز به طراحی بصری نهایی).

## معیار پذیرش

- [x] هر سه منبع ریسک بتوانند در یک لیست/heatmap واحد نمایش داده شوند.
- [x] امکان resolve کردن یک ریسک وجود داشته باشد.
