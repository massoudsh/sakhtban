from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from app.core import config as config_module
from app.services import file_storage


def _upload(content: bytes, content_type: str, filename: str = "photo.jpg") -> UploadFile:
    return UploadFile(filename=filename, file=BytesIO(content), headers=Headers({"content-type": content_type}))


@pytest.fixture
def isolated_settings(tmp_path, monkeypatch):
    """آپلود را روی یک پوشه‌ی موقت ایزوله می‌کند تا تست به دیسک واقعی پروژه دست نزند."""
    settings = config_module.Settings(upload_dir=str(tmp_path), max_upload_size_mb=1)
    monkeypatch.setattr(file_storage, "get_settings", lambda: settings)
    return settings


def test_save_upload_writes_file_and_returns_url(isolated_settings):
    upload = _upload(b"fake-jpeg-bytes", "image/jpeg")

    stored = file_storage.save_upload(upload, project_id="proj-1", kind="photo")

    assert stored.url.startswith(f"{isolated_settings.upload_public_path}/proj-1/")
    assert stored.url.endswith(".jpg")
    assert stored.content_type == "image/jpeg"
    assert stored.size_bytes == len(b"fake-jpeg-bytes")


def test_save_upload_rejects_disallowed_content_type(isolated_settings):
    upload = _upload(b"not-audio", "application/zip", filename="malware.zip")

    with pytest.raises(HTTPException) as exc_info:
        file_storage.save_upload(upload, project_id="proj-1", kind="voice")

    assert exc_info.value.status_code == 400


def test_save_upload_rejects_unknown_kind(isolated_settings):
    upload = _upload(b"data", "image/jpeg")

    with pytest.raises(HTTPException) as exc_info:
        file_storage.save_upload(upload, project_id="proj-1", kind="unknown")

    assert exc_info.value.status_code == 400


def test_save_upload_rejects_oversized_file_and_cleans_up(isolated_settings, tmp_path):
    too_big = b"x" * (2 * 1024 * 1024)  # 2MB > 1MB limit ست‌شده در isolated_settings
    upload = _upload(too_big, "image/jpeg")

    with pytest.raises(HTTPException) as exc_info:
        file_storage.save_upload(upload, project_id="proj-1", kind="photo")

    assert exc_info.value.status_code == 413
    assert list((tmp_path / "proj-1").iterdir()) == []
