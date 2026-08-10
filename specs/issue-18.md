# Issue #18 — ساخت خط زمانی تصمیم‌ها (Decision Timeline)

> فاز ۴ — Decision Log و پیشگیری از اختلاف · [GitHub Issue #18](https://github.com/massoudsh/sakhtban/issues/18)

## مسئله

مدیر پروژه باید بتواند تاریخچه‌ی تصمیم‌های پروژه را به‌ترتیب زمانی با پرچم‌های ابهام ببیند.

## طرح فنی

اندپوینت `GET /decisions/{project_id}/timeline` تصمیم‌ها را بر اساس `decision_date` مرتب برمی‌گرداند؛ کامپوننت `DecisionTimeline` هر تصمیم را با مسئول، وضعیت و پرچم‌های ابهام (رنگ قرمز) رسم می‌کند.

## فایل‌های کد مرتبط

- `backend/app/routers/decisions.py (decision_timeline)`
- `frontend/src/app/projects/[projectId]/decisions/page.tsx`
- `frontend/src/components/DecisionTimeline.tsx`

## وضعیت

کامل.

## معیار پذیرش

- [x] تصمیم‌ها به‌ترتیب تاریخ (تصمیم‌های بدون تاریخ در انتها) نمایش داده شوند.
