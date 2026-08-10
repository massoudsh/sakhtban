"""روتر انحراف و action item (issue #3, #5)."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.deviation import ActionItem, Deviation
from app.schemas.deviation import ActionItemOut, ActionItemUpdate, DeviationOut
from app.services.action_item_generator import build_action_item_for_deviation

router = APIRouter(prefix="/deviations", tags=["deviations"])


@router.get("/{project_id}", response_model=list[DeviationOut])
def list_deviations(project_id: uuid.UUID, db: Session = Depends(get_db)) -> list[Deviation]:
    stmt = select(Deviation).where(Deviation.project_id == project_id)
    return list(db.scalars(stmt))


@router.post("/{deviation_id}/generate-action-item", response_model=ActionItemOut, status_code=status.HTTP_201_CREATED)
def generate_action_item(deviation_id: uuid.UUID, db: Session = Depends(get_db)) -> ActionItem:
    """تولید خودکار Action Item از یک انحراف (issue #5)."""
    deviation = db.get(Deviation, deviation_id)
    if not deviation:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "انحراف پیدا نشد.")

    action_item = build_action_item_for_deviation(deviation)
    if action_item is None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "شدت این انحراف برای تولید خودکار action item کافی نیست."
        )

    db.add(action_item)
    db.commit()
    db.refresh(action_item)
    return action_item


action_router = APIRouter(prefix="/action-items", tags=["action-items"])


@action_router.get("/{project_id}", response_model=list[ActionItemOut])
def list_action_items(project_id: uuid.UUID, db: Session = Depends(get_db)) -> list[ActionItem]:
    stmt = select(ActionItem).where(ActionItem.project_id == project_id)
    return list(db.scalars(stmt))


@action_router.patch("/{action_item_id}", response_model=ActionItemOut)
def update_action_item(
    action_item_id: uuid.UUID, payload: ActionItemUpdate, db: Session = Depends(get_db)
) -> ActionItem:
    item = db.get(ActionItem, action_item_id)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Action item پیدا نشد.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item
