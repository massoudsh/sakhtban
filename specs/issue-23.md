# Issue #23 — موتور punch list خودکار و پیگیری اصلاح

> فاز ۵ — QA Copilot و کنترل کیفیت اجرا · [GitHub Issue #23](https://github.com/massoudsh/sakhtban/issues/23)

## مسئله

بعد از ثبت ایراد، باید چرخه‌ی اصلاح (پیمانکار اصلاح می‌کند → ناظر تأیید/رد می‌کند) رهگیری شود.

## طرح فنی

`POST /qa/defects/{id}/submit-fix` عکس بعد از اصلاح را ثبت و وضعیت را `fixed` می‌کند. `POST /qa/defects/{id}/verify` یا تأیید می‌کند (→ `verified`, punch item بسته می‌شود) یا رد می‌کند (→ `reopened`, شمارنده‌ی rework افزایش می‌یابد — ورودی مستقیم موتور rework issue #24).

## فایل‌های کد مرتبط

- `backend/app/routers/qa.py (submit_fix, verify_fix, punch_list)`
- `frontend/src/app/projects/[projectId]/qa/page.tsx`
- `frontend/src/components/PunchList.tsx`

## وضعیت

کامل.

## معیار پذیرش

- [x] رد شدن اصلاح، reopened_count را افزایش دهد و وضعیت را reopened کند.
