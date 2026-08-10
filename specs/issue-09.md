# Issue #9 — Import برنامه‌ی زمان‌بندی (Primavera XER / MS Project)

> فاز ۱ — اتصال برنامه‌ی زمان‌بندی · [GitHub Issue #9](https://github.com/massoudsh/sakhtban/issues/9)

## مسئله

مدیر پروژه باید بتواند فایل خروجی Primavera یا MS Project را مستقیم import کند، بدون ورود دستی.

## طرح فنی

پارسر XER جدول‌های `TASK`/`TASKPRED` را از فرمت tab-delimited خودش می‌خواند (بدون کتابخانه‌ی خارجی). برای MS Project از فرمت باز MSPDI XML استفاده شده (نه .mpp باینری که نیازمند MPXJ/JVM است) — تصمیم فنی مستند در کد. هر دو پارسر خروجی یکسان (task + dependency) تولید می‌کنند که در `ScheduleTask`/`TaskDependency` ذخیره می‌شود.

## فایل‌های کد مرتبط

- `backend/app/services/schedule_import/xer_parser.py`
- `backend/app/services/schedule_import/msproject_parser.py`
- `backend/app/routers/schedule.py`
- `backend/tests/test_xer_parser.py`
- `backend/tests/test_msproject_parser.py`

## وضعیت

کامل و تست‌شده برای XER و MSPDI XML. پشتیبانی مستقیم .mpp در scope فعلی نیست.

## معیار پذیرش

- [x] تسک‌ها و وابستگی‌ها از فایل نمونه‌ی XER درست پارس شوند.
- [x] خلاصه‌ی پروژه (UID=0) در MSPDI به‌عنوان تسک واقعی شمرده نشود.
