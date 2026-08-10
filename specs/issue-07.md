# Issue #7 — احراز هویت و مدیریت چندپروژه‌ای (multi-project workspace)

> فاز ۰ — Wedge MVP · [GitHub Issue #7](https://github.com/massoudsh/sakhtban/issues/7)

## مسئله

هر کاربر باید بتواند در چند پروژه با نقش‌های متفاوت عضو باشد و دسترسی جدا داشته باشد.

## طرح فنی

`User`/`ProjectMember`/`ProjectRole` (owner/manager/contributor/viewer) مدل رابطه‌ی چندبه‌چند را می‌سازند. JWT با `python-jose`/`PyJWT` صادر می‌شود؛ `get_current_user` dependency روی روترهای حساس (مثل ساخت پروژه) اعمال شده. رمز عبور با bcrypt هش می‌شود.

## فایل‌های کد مرتبط

- `backend/app/models/project.py`
- `backend/app/core/security.py`
- `backend/app/core/deps.py`
- `backend/app/routers/auth.py`
- `backend/app/routers/projects.py`
- `frontend/src/app/login/page.tsx`

## وضعیت

کامل برای MVP — رفرش توکن و rate limiting در production لازم است.

## معیار پذیرش

- [x] ثبت‌نام و ورود کاربر با JWT کار کند.
- [x] فقط owner/manager بتوانند عضو جدید به پروژه اضافه کنند.
