from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth.routes import get_current_user  # ✅ 새롭게 import
import models.competition
import schemas.competition
from auth.models import User
from fastapi import HTTPException
from models.bodyfat import BodyfatHistory
from schemas.competition import CompetitionCurrent
from datetime import date



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

# ✅ 가장 가까운 대회 정보 + 최신 체지방률 조회
@router.get("/current", response_model=CompetitionCurrent)
def get_current_competition(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    # 1. 가장 가까운 대회 가져오기
    competition = (
        db.query(models.competition.CompetitionHistory)
        .filter(models.competition.CompetitionHistory.user_id == current_user.id)
        .filter(models.competition.CompetitionHistory.competition_date >= today)
        .order_by(models.competition.CompetitionHistory.competition_date.asc())
        .first()
    )

    if not competition:
        raise HTTPException(status_code=404, detail="다가오는 대회가 없습니다.")

    # 2. 최신 체지방률 기록 가져오기
    bodyfat = (
        db.query(BodyfatHistory)
        .filter(BodyfatHistory.user_id == current_user.id)
        .order_by(BodyfatHistory.record_date.desc())
        .first()
    )

    if not bodyfat:
        raise HTTPException(status_code=404, detail="체지방 기록이 없습니다.")

    # 3. 문자열 '%' 제거하고 float로 변환
    try:
        current_bf = float(bodyfat.bodyfat_percent.replace('%', ''))
    except:
        current_bf = 0.0

    # 4. 다이어트 진행률 계산 (초기 체지방률은 임시로 25%)
    start_bf = 25.0
    target_bf = competition.target_bodyfat if competition.target_bodyfat is not None else 10.0

    try:
        if target_bf != start_bf:
            progress = max(0, min(100, (start_bf - current_bf) / (start_bf - target_bf) * 100))
        else:
            progress = 0.0
    except Exception as e:
        print("🚨 진행률 계산 중 오류 발생:", e)
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
