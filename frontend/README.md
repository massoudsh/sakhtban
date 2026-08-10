# Sakhtban Frontend (اسکلت اولیه)

پنل وب Sakhtban با Next.js 14 (App Router) + TypeScript، بدون کتابخانه‌ی state management سنگین.

## صفحات پیاده‌سازی‌شده

| مسیر | فیچر | Issue |
|---|---|---|
| `/login` | ورود کاربر | #7 |
| `/projects/[projectId]/reports` | ثبت گزارش کارگاه (کانال وب) | #6, #2 |
| `/projects/[projectId]/schedule` | نمایش برنامه‌ی زمان‌بندی import شده | #9, #10 |
| `/projects/[projectId]/risk-heatmap` | Risk Heatmap یکپارچه (هر سه لایه) | #4, #19, #25 |
| `/projects/[projectId]/decisions` | خط زمانی تصمیم‌ها + پرچم ابهام | #18 |
| `/projects/[projectId]/qa` | Punch List | #23 |

## اجرا (روی سرور، نه داخل کانتینر ابزار)

```bash
cp .env.example .env.local   # NEXT_PUBLIC_API_BASE_URL را تنظیم کن
npm install
npm run dev
```

## نکات فنی

- اپ موبایل ثبت ایراد (issue #22) در scope این وب‌اپ نیست — نیازمند تصمیم جدا درباره‌ی
  استک موبایل (React Native / Flutter) است؛ فعلاً معادل وبِ آن (فرم ثبت گزارش، punch list)
  پیاده شده تا API قابل تست باشد.
- احراز هویت فعلاً ساده (JWT در localStorage) است؛ برای پروڈاکشن باید httpOnly cookie
  و refresh token اضافه شود.
