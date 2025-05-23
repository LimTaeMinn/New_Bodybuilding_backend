from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth.routes import get_current_user  # ✅ 새롭게 import
import models.competition
import schemas.competition
from auth.models import User


router = APIRouter(
    prefix="/competition",
    tags=["Competition"]
)

# ✅ 대회 기록 등록
@router.post("/")
def create_competition_record(
    record: schemas.competition.CompetitionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_record = models.competition.CompetitionHistory(
        **record.dict(),
        user_id=current_user.id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# ✅ 월별 대회 기록 조회
@router.get("/month/{year}/{month}")
def get_monthly_competitions(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(models.competition.CompetitionHistory)\
        .filter(models.competition.CompetitionHistory.user_id == current_user.id)\
        .filter(models.competition.CompetitionHistory.competition_date.between(
            f"{year}-{month:02d}-01", f"{year}-{month:02d}-31"
        )).all()
    return records
