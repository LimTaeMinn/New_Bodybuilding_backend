from pydantic import BaseModel
from datetime import date
from typing import Optional

# ✅ 대회 기록을 새로 생성할 때 사용할 스키마
class CompetitionCreate(BaseModel):
    title: str           # 대회 이름
    category: str        # 대회 종목
    target_rank: str     # 목표 등수
    actual_rank: str     # 실제 수상 등수
    competition_date: date  # 대회 날짜

# ✅ 대회 기록 수정 시 사용할 스키마 (모든 필드 Optional)
class CompetitionUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    target_rank: Optional[str] = None
    actual_rank: Optional[str] = None
    competition_date: Optional[date] = None

# ✅ DB에서 읽어올 때 사용할 응답용 스키마
class CompetitionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    category: str
    target_rank: str
    actual_rank: str
    competition_date: date

    class Config:
        orm_mode = True

# ✅ "My Contest"에서 사용할 응답용 스키마
class CompetitionCurrent(BaseModel):
    d_day: int                    # D-day (예: 99)
    title: str                    # 대회 이름
    category: str                 # 대회 종목
    target_rank: str              # 목표 등수
    target_bodyfat: float         # 목표 체지방률
    current_bodyfat: float        # 현재 체지방률
    progress_percent: float       # 다이어트 진행률 (%)

    class Config:
        orm_mode = True