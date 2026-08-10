"""روتر پروژه و عضویت چندپروژه‌ای (issue #7)."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.project import Project, ProjectMember, ProjectRole, User
from app.schemas.project import ProjectCreate, ProjectMemberCreate, ProjectMemberOut, ProjectOut

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Project:
    project = Project(name=payload.name, location=payload.location)
    db.add(project)
    db.flush()

    db.add(ProjectMember(project_id=project.id, user_id=current_user.id, role=ProjectRole.OWNER))
    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=list[ProjectOut])
def list_my_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[Project]:
    stmt = (
        select(Project)
        .join(ProjectMember, ProjectMember.project_id == Project.id)
        .where(ProjectMember.user_id == current_user.id)
    )
    return list(db.scalars(stmt))


@router.post("/{project_id}/members", response_model=ProjectMemberOut, status_code=status.HTTP_201_CREATED)
def add_member(
    project_id: uuid.UUID,
    payload: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectMember:
    membership = db.scalar(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id, ProjectMember.user_id == current_user.id
        )
    )
    if not membership or membership.role not in (ProjectRole.OWNER, ProjectRole.MANAGER):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "اجازه‌ی افزودن عضو به این پروژه را ندارید.")

    member = ProjectMember(project_id=project_id, user_id=payload.user_id, role=payload.role)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member
