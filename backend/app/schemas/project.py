"""اسکیمای پروژه و عضویت (issue #7)."""
import uuid

from pydantic import BaseModel

from app.models.project import ProjectRole


class ProjectCreate(BaseModel):
    name: str
    location: str | None = None


class ProjectOut(BaseModel):
    id: uuid.UUID
    name: str
    location: str | None = None
    is_archived: bool

    model_config = {"from_attributes": True}


class ProjectMemberCreate(BaseModel):
    user_id: uuid.UUID
    role: ProjectRole = ProjectRole.CONTRIBUTOR


class ProjectMemberOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    role: ProjectRole

    model_config = {"from_attributes": True}
