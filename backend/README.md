# Sakhtban Backend (اسکلت اولیه)

FastAPI + SQLAlchemy 2.0 + PostgreSQL + Alembic. پوشش کد برای هر ۲۶ ایشوی باز پروژه در
`/project/specs/` مستند شده — این README فقط نحوه‌ی اجرا را توضیح می‌دهد.

## اجرا (روی سرور، نه داخل کانتینر ابزار — نیاز به PostgreSQL واقعی دارد)

```bash
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# ساخت اولین migration و اجرای آن (نیاز به PostgreSQL در حال اجرا)
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

uvicorn app.main:app --reload
```

مستندات تعاملی API بعد از اجرا: `/docs` (Swagger) و `/redoc`.

## تست‌ها

تست‌های واحد فقط منطق خالص (پارسرها، موتورهای rule-based) را پوشش می‌دهند و نیازی به
دیتابیس ندارند:

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## ساختار

```
app/
  core/        تنظیمات، دیتابیس، امنیت/JWT
  models/      مدل‌های SQLAlchemy — یک فایل به‌ازای هر حوزه (project, report, schedule,
               deviation, cost, decision, qa, onboarding)
  schemas/     اسکیمای Pydantic برای request/response
  routers/     اندپوینت‌های FastAPI
  services/    منطق کسب‌وکار: پارسرهای NLP، موتورهای تشخیص انحراف/ابهام/rework،
               پیش‌بینی زنجیره‌ای تأخیر، تولید گزارش اجرایی
```

## وضعیت فعلی — چه چیزی واقعی است، چه چیزی نیاز به توسعه دارد

- **کامل و تست‌شده:** مدل داده‌ی همه‌ی حوزه‌ها، پارسر NLP فارسی (heuristic)، موتور تشخیص
  انحراف، موتور ابهام تصمیم، موتور rework pattern، پارسر XER/MSPDI، پیش‌بینی زنجیره‌ای
  تأخیر (forward-pass ساده)، همه‌ی روترهای CRUD پایه.
- **نیاز به تکمیل قبل از production:** migration واقعی روی PostgreSQL (باید روی سرور
  اجرا شود)، سخت‌گیری بیشتر روی auth (رفرش توکن، rate limit)، جایگزینی پارسرهای heuristic
  با NLP آموزش‌دیده در صورت نیاز به دقت بالاتر، رندر PDF گزارش‌های اجرایی، اتصال واقعی
  ربات تلگرام (webhook فعلی ساختار پیام را می‌پذیرد ولی bind کردن chat_id به project_id
  پیاده نشده).
