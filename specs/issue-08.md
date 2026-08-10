# Issue #8 — Landing page و آنبوردینگ اولین پایلوت‌ها

> فاز ۰ — Wedge MVP · [GitHub Issue #8](https://github.com/massoudsh/sakhtban/issues/8)

## مسئله

لندینگ‌پیج باید بتواند لید پایلوت جمع کند، نه فقط معرفی محصول باشد.

## طرح فنی

لندینگ‌پیج (`docs/index.html`) یک فرم «درخواست پایلوت» دارد که با `fetch` مستقیم به `POST /onboarding/pilot-lead` وصل می‌شود (مدل `PilotLead`). آدرس بک‌اند از طریق `window.SAKHTBAN_API_BASE` (پیش‌فرض `https://api.sakhtban.ir`) قابل تنظیم است و باید بعد از استقرار واقعی سرور به‌روزرسانی شود.

## فایل‌های کد مرتبط

- `docs/index.html` — فرم + اتصال JS به API
- `backend/app/models/onboarding.py`
- `backend/app/routers/onboarding.py`

## وضعیت

کامل — بک‌اند و فرم لندینگ به هم وصل‌اند. تنها باقی‌مانده تنظیم `API_BASE` واقعی بعد از استقرار سرور است (خارج از این تسک).

## معیار پذیرش

- [x] لید با نام شرکت، تماس، تلفن و پیام اختیاری ذخیره شود.
