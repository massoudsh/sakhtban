# Issue #12 — ماژول رهگیری خرید و تأمین (procurement tracking)

> فاز ۲ — هزینه و خرید · [GitHub Issue #12](https://github.com/massoudsh/sakhtban/issues/12)

## مسئله

تأخیر در تأمین کالا یکی از رایج‌ترین علت‌های تأخیر پروژه است و باید جدا رهگیری شود.

## طرح فنی

`ProcurementItem` وضعیت (requested/ordered/in_transit/delivered/delayed) و تاریخ تحویل مورد انتظار/واقعی را نگه می‌دارد و می‌تواند به یک `ScheduleTask` لینک شود. اندپوینت `/procurement/{project_id}/delayed` اقلامی که از تاریخ تحویل موردانتظار گذشته‌اند را برمی‌گرداند.

## فایل‌های کد مرتبط

- `backend/app/models/cost.py (ProcurementItem)`
- `backend/app/routers/cost.py (procurement_router)`

## وضعیت

کامل.

## معیار پذیرش

- [x] اقلام دارای expected_delivery گذشته و بدون actual_delivery در لیست delayed دیده شوند.
