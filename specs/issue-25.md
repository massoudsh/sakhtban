# Issue #25 — اتصال QA Copilot به Risk Heatmap موجود

> فاز ۵ — QA Copilot و کنترل کیفیت اجرا · [GitHub Issue #25](https://github.com/massoudsh/sakhtban/issues/25)

## مسئله

الگوی تکرار ایراد باید مستقیم در همان Risk Heatmap دیده شود، نه در یک داشبورد QA جدا.

## طرح فنی

`risk_item_from_rework_pattern` هر `ReworkPattern` بالای آستانه‌ی هشدار را به `RiskItem` با `source_type=QA_REWORK_PATTERN` تبدیل می‌کند. این تبدیل داخل `POST /qa/{project_id}/analyze-rework-patterns` انجام می‌شود.

## فایل‌های کد مرتبط

- `backend/app/services/risk_heatmap.py (risk_item_from_rework_pattern)`
- `backend/app/routers/qa.py (analyze_rework_patterns)`

## وضعیت

کامل — وابسته به issue #4 (RiskItem model) که از قبل موجود است.

## معیار پذیرش

- [x] اجرای analyze-rework-patterns روی داده‌ی الگودار، RiskItem جدید در heatmap تولید کند.
