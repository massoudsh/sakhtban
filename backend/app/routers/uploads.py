"""روتر آپلود فایل — زیرساخت مشترک عکس/صدای ایراد QA و سایر پیوست‌ها (تکمیل issue #22)."""
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.project import ProjectMember, User
from app.schemas.uploads import UploadOut
from app.services.file_storage import save_upload

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/{project_id}", response_model=UploadOut, status_code=status.HTTP_201_CREATED)
def upload_file(
    project_id: uuid.UUID,
    kind: str = "photo",
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UploadOut:
    """آپلود عکس/صدا/سند از اپ موبایل یا وب. فقط اعضای پروژه اجازه دارند."""
    membership = db.scalar(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id, ProjectMember.user_id == current_user.id
        )
    )
    if not membership:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "عضو این پروژه نیستید.")

    stored = save_upload(file, project_id=str(project_id), kind=kind)
    return UploadOut(url=stored.url, content_type=stored.content_type, size_bytes=stored.size_bytes)
