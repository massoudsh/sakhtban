# Issue #22 — اپ موبایل ثبت ایراد (عکس + موقعیت + توضیح)

> فاز ۵ — QA Copilot و کنترل کیفیت اجرا · [GitHub Issue #22](https://github.com/massoudsh/sakhtban/issues/22)

## مسئله

ثبت ایراد باید در محل کارگاه، سریع و با موبایل انجام شود. باید آفلاین‌فرست کار کند
(اینترنت ضعیف کارگاه) و سریع‌تر از واتساپ/دفترچه باشد.

## طرح فنی

استک انتخاب‌شده: **React Native (Expo)** — یک codebase برای iOS/اندروید، سازگار با
TypeScript که بقیه‌ی frontend هم با آن نوشته شده. اپ در `mobile/` به‌صورت اسکلت کامل
نوشته شده:

- **دوربین**: `expo-camera` برای گرفتن عکس ایراد.
- **موقعیت**: هم GPS خودکار (`expo-location`) و هم پین دستی روی تصویر پلان طبقه
  (`FloorPlanPicker` — مختصات نسبی ۰ تا ۱، برای داخل ساختمان که GPS دقیق نیست).
- **توضیح**: متنی (اجباری) + صوتی اختیاری با `expo-av` (ضبط و پیوست).
- **پیمانکار/شدت**: ورودی متنی پیمانکار + `SeverityPicker` سه‌حالته.
- **آفلاین‌فرست**: `src/lib/offlineQueue.ts` — تلاش مستقیم برای ارسال؛ اگر آفلاین/شکست
  خورد، در صف محلی (`AsyncStorage`) می‌ماند و با برگشت اتصال (`NetInfo`) خودکار
  flush می‌شود؛ کاربر هم می‌تواند دستی sync کند.

برای پشتیبانی از توضیح صوتی و پین پلان طبقه، مدل `Defect` سه فیلد جدید گرفت:
`voice_note_url`, `floor_plan_x`, `floor_plan_y` (نیازمند alembic migration به‌روزشده).

## محدودیت صادقانه

آپلود واقعی فایل (عکس/صدا) به یک object storage عمومی (S3/MinIO) در این تسک نیست —
`photo_before_url`/`voice_note_url` فعلاً URI محلی دستگاه است، همان الگوی ساده‌ای که
در فرم وب هم برای `photo_before_url` استفاده شده. جزئیات در `mobile/README.md`.
این پروژه فقط نوشته شده، نه `npm install`/build‌شده — طبق قاعده‌ی پروژه باید روی سرور
SSH یا ماشین توسعه اجرا شود.

## فایل‌های کد مرتبط

- `mobile/` — اپ کامل React Native/Expo (App.tsx, src/screens, src/components, src/lib)
- `backend/app/routers/qa.py (report_defect)`
- `backend/app/schemas/qa.py (DefectCreate)`
- `backend/app/models/qa.py (Defect.voice_note_url, floor_plan_x, floor_plan_y)`
- `backend/alembic/versions/25159ca33120_initial_schema.py`

## وضعیت

کامل — کد اپ موبایل نوشته شده (دوربین، GPS، پین پلان طبقه، صدا، صف آفلاین). فقط
باقی‌مانده: اجرا/build واقعی روی سرور (`npm install && npx expo start`، خارج از این
محیط ابزار) و در آینده اتصال به یک سرویس آپلود فایل واقعی.

## معیار پذیرش

- [x] اندپوینت ثبت ایراد، عکس/GPS/موقعیت/شدت را بپذیرد و PunchItem خودکار بسازد.
- [x] اپ موبایل بومی (React Native) با دوربین، GPS، پین روی پلان طبقه و توضیح متنی/صوتی.
- [x] رفتار آفلاین‌فرست — صف محلی + همگام‌سازی خودکار با برگشت اتصال.
