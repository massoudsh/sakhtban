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

## سرویس آپلود فایل

عکس/صدا با `POST /uploads/{project_id}?kind=photo|voice` (multipart، نیازمند توکن +
عضویت پروژه) آپلود می‌شود و بک‌اند فایل را روی دیسک محلی ذخیره و URL نسبی سرو‌شونده
(`/files/...`) برمی‌گرداند — `backend/app/services/file_storage.py` +
`backend/app/routers/uploads.py`. اپ موبایل قبل از `POST /qa/defects` هر URI محلی
(`file://`) را از همین اندپوینت آپلود می‌کند (`mobile/src/lib/offlineQueue.ts#resolveLocalUploads`)؛
اگر آفلاین باشد، آیتم با URI محلی در صف می‌ماند تا تلاش بعدی. جزئیات در `mobile/README.md`.

**محدودیت باقی‌مانده:** بک‌اند فعلاً local filesystem است، نه object storage واقعی
(S3/MinIO) — برای استقرار چندسروری باید `file_storage.py` به یک backend ابری وصل شود؛
رابط (`save_upload` → URL نسبی) طوری طراحی شده که این تغییر به روتر/کلاینت سرایت نکند.
این پروژه فقط نوشته شده، نه `npm install`/build‌شده — طبق قاعده‌ی پروژه باید روی سرور
SSH یا ماشین توسعه اجرا شود.

## فایل‌های کد مرتبط

- `mobile/` — اپ کامل React Native/Expo (App.tsx, src/screens, src/components, src/lib)
- `backend/app/routers/qa.py (report_defect)`
- `backend/app/routers/uploads.py`, `backend/app/services/file_storage.py`
- `backend/app/schemas/qa.py (DefectCreate)`
- `backend/app/models/qa.py (Defect.voice_note_url, floor_plan_x, floor_plan_y)`
- `backend/alembic/versions/25159ca33120_initial_schema.py`

## وضعیت

کامل — کد اپ موبایل نوشته شده (دوربین، GPS، پین پلان طبقه، صدا، صف آفلاین) و به سرویس
آپلود فایل واقعی وصل شده. فقط باقی‌مانده: اجرا/build واقعی روی سرور
(`npm install && npx expo start`، خارج از این محیط ابزار).

## معیار پذیرش

- [x] اندپوینت ثبت ایراد، عکس/GPS/موقعیت/شدت را بپذیرد و PunchItem خودکار بسازد.
- [x] اپ موبایل بومی (React Native) با دوربین، GPS، پین روی پلان طبقه و توضیح متنی/صوتی.
- [x] رفتار آفلاین‌فرست — صف محلی + همگام‌سازی خودکار با برگشت اتصال.
- [x] آپلود واقعی فایل (عکس/صدا) به بک‌اند به‌جای نگه‌داشتن URI محلی دستگاه.
