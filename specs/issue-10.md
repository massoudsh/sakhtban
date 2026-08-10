# Issue #10 — موتور تطبیق برنامه با واقعیت اجرا (schedule variance engine)

> فاز ۱ — اتصال برنامه‌ی زمان‌بندی · [GitHub Issue #10](https://github.com/massoudsh/sakhtban/issues/10)

## مسئله

بعد از import، باید واقعیت اجرا (actual/percent_complete) به‌طور مداوم با baseline مقایسه شود.

## طرح فنی

همان موتور issue #3 (`deviation_engine.py`) پایه‌ی این قابلیت است؛ اندپوینت `POST /schedule/{project_id}/detect-deviations` آن را روی همه‌ی تسک‌های یک پروژه اجرا و نتایج را در جدول `deviations` ذخیره می‌کند. صفحه‌ی وب `schedule` وضعیت هر تسک (baseline/actual/percent) را نمایش می‌دهد.

## فایل‌های کد مرتبط

- `backend/app/routers/schedule.py (run_deviation_detection)`
- `backend/app/services/deviation_engine.py`
- `frontend/src/app/projects/[projectId]/schedule/page.tsx`

## وضعیت

کامل.

## معیار پذیرش

- [x] اجرای اندپوینت روی یک پروژه، انحراف‌های جدید را در دیتابیس ثبت کند.
