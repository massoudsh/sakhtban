# Issue #8 — Landing page و آنبوردینگ اولین پایلوت‌ها

> فاز ۰ — Wedge MVP · [GitHub Issue #8](https://github.com/massoudsh/sakhtban/issues/8)

## مسئله

لندینگ‌پیج باید بتواند لید پایلوت جمع کند، نه فقط معرفی محصول باشد.

## طرح فنی

لندینگ‌پیج (`docs/index.html`) از قبل موجود است. مدل `PilotLead` + اندپوینت `POST /onboarding/pilot-lead` یک نقطه‌ی اتصال ساده برای فرم «درخواست پایلوت» فراهم می‌کند تا لندینگ بتواند به‌جای mailto صرف، مستقیم به backend وصل شود.

## فایل‌های کد مرتبط

- `docs/index.html (موجود)`
- `backend/app/models/onboarding.py`
- `backend/app/routers/onboarding.py`

## وضعیت

بک‌اند آماده؛ اتصال فرم لندینگ به این اندپوینت باقی مانده (فعلاً لندینگ mailto/لینک مستقیم دارد).

## معیار پذیرش

- [x] لید با نام شرکت، تماس، تلفن و پیام اختیاری ذخیره شود.
