"""روتر ثبت لید پایلوت از لندینگ‌پیج (issue #8)."""
import uuid

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.onboarding import PilotLead

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


class PilotLeadCreate(BaseModel):
    company_name: str
    contact_name: str
    phone: str
    email: EmailStr | None = None
    message: str | None = None


class PilotLeadOut(BaseModel):
    id: uuid.UUID

    model_config = {"from_attributes": True}


@router.post("/pilot-lead", response_model=PilotLeadOut, status_code=status.HTTP_201_CREATED)
def submit_pilot_lead(payload: PilotLeadCreate, db: Session = Depends(get_db)) -> PilotLead:
    lead = PilotLead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
