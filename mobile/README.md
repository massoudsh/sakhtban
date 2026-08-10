# سخت‌بان QA — اپ موبایل ثبت ایراد (issue #22)

اپ موبایل بومی React Native (با Expo) برای ثبت سریع ایراد کیفی در محل کارگاه:
عکس، موقعیت (GPS + پین روی پلان طبقه)، توضیح متنی/صوتی، پیمانکار مسئول و شدت.

## چرا React Native (Expo)

- یک codebase برای iOS و اندروید — تیم فعلی پروژه از قبل روی TypeScript/React کار می‌کند (frontend وب هم Next.js/TS است)، پس منحنی یادگیری کمتر است.
- Expo دسترسی آماده به دوربین (`expo-camera`)، GPS (`expo-location`) و ضبط صدا (`expo-av`) می‌دهد بدون نیاز به native module دستی.
- برای MVP، build سرویس‌های ابری Expo (EAS) امکان توزیع build آزمایشی بدون نیاز به Xcode/Android Studio محلی را می‌دهد.

## معماری آفلاین‌فرست

مشکل اصلی که این ایشو حل می‌کند: «اینترنت ضعیف کارگاه». به همین دلیل:

- هر ثبت ایراد اول تلاش می‌کند مستقیم به `POST /qa/defects` بفرستد (`src/lib/offlineQueue.ts#submitOrQueue`).
- اگر آفلاین باشد یا درخواست شکست بخورد، آیتم در یک صف محلی (`AsyncStorage`) ذخیره می‌شود.
- با `NetInfo`، هر بار اتصال برمی‌گردد صف به‌طور خودکار خالی می‌شود (`subscribeAutoFlush` در `App.tsx`).
- کاربر همیشه می‌تواند صف را دستی هم خالی کند (بنر بالای صفحه‌ی ثبت ایراد).

## آپلود فایل

عکس/صدا به‌صورت multipart به `POST /uploads/{project_id}?kind=photo|voice` آپلود می‌شود
(`src/lib/api.ts#uploadFile`) و بک‌اند فایل را روی دیسک محلی زیر `UPLOAD_DIR` ذخیره و
URL نسبی سرو‌شونده (زیر `/files/...`) برمی‌گرداند — پیاده‌سازی در
`backend/app/services/file_storage.py` + `backend/app/routers/uploads.py`.

آپلود در همان مسیر آفلاین‌فرست ادغام شده (`src/lib/offlineQueue.ts#resolveLocalUploads`):
قبل از فراخوانی `POST /qa/defects`، اگر `photo_before_url`/`voice_note_url` هنوز URI محلی
دستگاه باشد (`file://`)، اول آپلود می‌شود و URL واقعی سرور جایگزین آن می‌شود؛ اگر آپلود هم
(به‌خاطر آفلاین‌بودن) شکست بخورد، آیتم با همان URI محلی در صف می‌ماند تا تلاش بعدی.

**محدودیت باقی‌مانده:** بک‌اند فعلاً local filesystem است، نه object storage واقعی (S3/MinIO)؛
برای استقرار چندسروری/مقیاس‌پذیر باید `file_storage.py` به یک backend ابری وصل شود — رابط
(`save_upload` → URL نسبی) طوری طراحی شده که این تغییر به روتر/کلاینت‌ها سرایت نکند.

## اجرا (خارج از این محیط ابزار)

این پروژه فقط **نوشته شده**، نه build/run‌شده — طبق قاعده‌ی پروژه، `npm install` و اجرای Expo باید
روی سرور SSH یا ماشین توسعه انجام شود، نه داخل این کانتینر.

```bash
cd mobile
npm install
cp .env.example .env   # EXPO_PUBLIC_API_BASE_URL را به آدرس واقعی بک‌اند تنظیم کنید
npx expo start
```

سپس با اپ Expo Go (یا شبیه‌ساز) اسکن/اجرا کنید.

## فایل‌های کلیدی

- `App.tsx` — navigation + شروع گوش‌دادن به صف آفلاین.
- `src/lib/api.ts` — کلاینت fetch (معادل موبایل `frontend/src/lib/api.ts`).
- `src/lib/offlineQueue.ts` — صف آفلاین + auto-flush.
- `src/screens/NewDefectScreen.tsx` — صفحه‌ی اصلی ثبت ایراد (دوربین، GPS، پلان طبقه، صدا).
- `src/components/FloorPlanPicker.tsx` — انتخاب موقعیت با لمس روی تصویر پلان.

## وابستگی به بک‌اند

از همان API موجود استفاده می‌کند؛ سه فیلد جدید برای این اپ به مدل `Defect` اضافه شد:
`voice_note_url`، `floor_plan_x`، `floor_plan_y` (به‌روزرسانی در `backend/app/models/qa.py`،
`backend/app/schemas/qa.py` و `backend/alembic/versions/25159ca33120_initial_schema.py`).
