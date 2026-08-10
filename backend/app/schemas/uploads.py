"""اسکیمای پاسخ سرویس آپلود فایل (عکس/صدای QA و سایر پیوست‌ها)."""
from pydantic import BaseModel


class UploadOut(BaseModel):
    url: str
    content_type: str
    size_bytes: int
