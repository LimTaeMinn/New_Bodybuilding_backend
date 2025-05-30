from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth.models import BodyfatHistory
from schemas.bodyfat import BodyfatCreate, BodyfatRecord
from auth.models import User
from auth.utils import get_current_user
from datetime import date

router = APIRouter(prefix="/bodyfat", tags=["Bodyfat"])

@router.post("/", response_model=BodyfatRecord)
def create_record(data: BodyfatCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = BodyfatHistory(
        user_id=current_user.id,
        bodyfat_percent=data.bodyfat_percent,
        confidence=data.confidence,
        recommended_diet=data.recommended_diet,
        recommended_workout=data.recommended_workout,
        image_url=data.image_url
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/history", response_model=list[BodyfatRecord])
def get_records_by_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(BodyfatHistory).filter(BodyfatHistory.user_id == current_user.id).order_by(BodyfatHistory.record_date.desc()).all()
