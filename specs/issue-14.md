# Issue #14 — گزارش‌گیری اجرایی برای کارفرما و سرمایه‌گذار

> فاز ۳ — لایه‌ی Execution Intelligence · [GitHub Issue #14](https://github.com/massoudsh/sakhtban/issues/14)

## مسئله

کارفرما/سرمایه‌گذار به یک خلاصه‌ی سطح‌بالا نیاز دارند، نه جزئیات فنی خام.

## طرح فنی

`build_executive_report` سه بخش می‌سازد: مهم‌ترین ریسک‌های باز (از Risk Heatmap)، انحراف‌های باز، و action item های در جریان. خروجی یک payload JSON ساخت‌یافته (`ExecutiveReport.to_dict`) است؛ رندر نهایی PDF عمداً در این لایه انجام نشده تا سرویس به موتور رندر سنگین وابسته نباشد.

## فایل‌های کد مرتبط

- `backend/app/services/reports/report_builder.py`
- `backend/app/services/reports/executive_report.py`
- `backend/app/routers/reports_exec.py`

## وضعیت

کامل برای خروجی JSON؛ رندر PDF/چاپ در فاز بعد.

## معیار پذیرش

- [x] گزارش شامل top-N ریسک، انحراف‌های باز و action item های باز باشد.
