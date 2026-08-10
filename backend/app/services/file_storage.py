"""سرویس آپلود فایل — ذخیره‌سازی محلی روی دیسک برای عکس/صدای ایراد QA و سایر پیوست‌ها.

فعلاً بک‌اند local filesystem است (زیر `UPLOAD_DIR`، سرو شده از مسیر `upload_public_path`).
این جداسازی عمدی است: اگر بعداً به object storage واقعی (S3/MinIO) نیاز شد، فقط همین
فایل عوض می‌شود؛ روتر و بقیه‌ی برنامه با URL نسبی برگشتی کار می‌کنند و تغییری لازم ندارند.
"""
import uuid
from dataclasses import dataclass
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings

# نوع‌های محتوای مجاز به تفکیک کاربرد آپلود.
ALLOWED_CONTENT_TYPES: dict[str, set[str]] = {
    "photo": {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"},
    "voice": {"audio/m4a", "audio/mp4", "audio/mpeg", "audio/aac", "audio/x-m4a", "audio/wav", "audio/webm"},
    "document": {"application/pdf", "image/jpeg", "image/png"},
}

_EXTENSION_BY_CONTENT_TYPE: dict[str, str] = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/heic": "heic",
    "image/heif": "heif",
    "audio/m4a": "m4a",
    "audio/mp4": "m4a",
    "audio/mpeg": "mp3",
    "audio/aac": "aac",
    "audio/x-m4a": "m4a",
    "audio/wav": "wav",
    "audio/webm": "webm",
    "application/pdf": "pdf",
}

_CHUNK_SIZE = 1024 * 1024


@dataclass
class StoredFile:
    url: str
    content_type: str
    size_bytes: int


def save_upload(file: UploadFile, project_id: str, kind: str) -> StoredFile:
    """اعتبارسنجی نوع/حجم فایل و ذخیره‌ی آن زیر `UPLOAD_DIR/<project_id>/`.

    یک نام تصادفی (uuid4) برای فایل ذخیره‌شده تولید می‌کند (بدون اعتماد به نام فایل کلاینت)
    و URL نسبیِ قابل‌سرو (زیر `upload_public_path`) برمی‌گرداند. حجم فایل به‌صورت stream
    بررسی می‌شود تا فایل بزرگ‌تر از حد مجاز کامل روی دیسک نوشته نشود.
    """
    settings = get_settings()

    allowed = ALLOWED_CONTENT_TYPES.get(kind)
    if allowed is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "نوع آپلود (kind) نامعتبر است.")
    if file.content_type not in allowed:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, f"نوع فایل «{file.content_type}» برای «{kind}» مجاز نیست."
        )

    extension = _EXTENSION_BY_CONTENT_TYPE.get(file.content_type, "bin")
    max_bytes = settings.max_upload_size_mb * 1024 * 1024

    project_dir = Path(settings.upload_dir) / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    dest_name = f"{uuid.uuid4()}.{extension}"
    dest_path = project_dir / dest_name

    size = 0
    try:
        with open(dest_path, "wb") as out:
            while chunk := file.file.read(_CHUNK_SIZE):
                size += len(chunk)
                if size > max_bytes:
                    raise HTTPException(
                        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        f"حجم فایل از {settings.max_upload_size_mb} مگابایت مجاز بیشتر است.",
                    )
                out.write(chunk)
    except HTTPException:
        dest_path.unlink(missing_ok=True)
        raise
    finally:
        file.file.close()

    return StoredFile(
        url=f"{settings.upload_public_path}/{project_id}/{dest_name}",
        content_type=file.content_type,
        size_bytes=size,
    )
