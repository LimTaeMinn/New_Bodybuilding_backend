from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from auth.routes import get_current_user
from auth.models import User

import models.competition
import schemas.competition

router = APIRouter(
    prefix="/competition",
    tags=["Competition"]
)

# ✅ 대회 기록 생성
@router.post(
    "/",
    response_model=schemas.competition.CompetitionResponse,
    status_code=status.HTTP_201_CREATED
)
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
@router.get(
    "/month/{year}/{month}",
    response_model=list[schemas.competition.CompetitionResponse]
)
def get_monthly_competitions(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start = date(year, month, 1)
    import calendar
    last_day = calendar.monthrange(year, month)[1]
    end = date(year, month, last_day)
    records = (
        db.query(models.competition.CompetitionHistory)
          .filter(models.competition.CompetitionHistory.user_id == current_user.id)
          .filter(models.competition.CompetitionHistory.competition_date.between(start, end))
          .all()
    )
    return records

# ✅ 다가오는 대회 + 진행률 조회
@router.get(
    "/current",
    response_model=schemas.competition.CompetitionCurrent
)
def get_current_competition(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    competition = (
        db.query(models.competition.CompetitionHistory)
          .filter(models.competition.CompetitionHistory.user_id == current_user.id)
          .filter(models.competition.CompetitionHistory.competition_date >= today)
          .order_by(models.competition.CompetitionHistory.competition_date.asc())
          .first()
    )
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="다가오는 대회가 없습니다.")

    from models.bodyfat import BodyfatHistory
    bodyfat = (
        db.query(BodyfatHistory)
          .filter(BodyfatHistory.user_id == current_user.id)
          .order_by(BodyfatHistory.record_date.desc())
          .first()
    )
    if not bodyfat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="체지방 기록이 없습니다.")

    try:
        current_bf = float(bodyfat.bodyfat_percent.replace('%', ''))
    except:
        current_bf = 0.0

    start_bf = 25.0
    target_bf = competition.target_bodyfat or 10.0
    if target_bf != start_bf:
        progress = max(0.0, min(100.0, (start_bf - current_bf) / (start_bf - target_bf) * 100.0))
    else:
        progress = 0.0

    return {
        "d_day": (competition.competition_date - today).days,
        "title": competition.title,
        "category": competition.category,
        "target_rank": competition.target_rank,
        "target_bodyfat": target_bf,
        "current_bodyfat": current_bf,
        "progress_percent": round(progress, 1)
    }

# ✅ 대회 기록 수정
@router.put(
    "/{comp_id}",
    response_model=schemas.competition.CompetitionResponse,
    status_code=status.HTTP_200_OK
)
def update_competition_record(
    comp_id: int,
    payload: schemas.competition.CompetitionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comp = (
        db.query(models.competition.CompetitionHistory)
          .filter(models.competition.CompetitionHistory.id == comp_id)
          .filter(models.competition.CompetitionHistory.user_id == current_user.id)
          .first()
    )
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 대회 기록을 찾을 수 없습니다.")

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comp, field, value)
    db.commit()
    db.refresh(comp)
    return comp

# ✅ 대회 기록 삭제
@router.delete(
    "/{comp_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_competition_record(
    comp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comp = (
        db.query(models.competition.CompetitionHistory)
          .filter(models.competition.CompetitionHistory.id == comp_id)
          .filter(models.competition.CompetitionHistory.user_id == current_user.id)
          .first()
    )
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 대회 기록을 찾을 수 없습니다.")
    db.delete(comp)
    db.commit()
    return