from pydantic import BaseModel
from datetime import date

# ✅ 대회 기록을 새로 생성할 때 사용할 스키마
class CompetitionCreate(BaseModel):
    title: str           # 대회 이름
    category: str        # 대회 종목
    target_rank: str     # 목표 등수
    actual_rank: str     # 실제 수상 등수
    competition_date: date  # 대회 날짜

# ✅ DB에서 읽어올 때 사용할 응답용 스키마
class Competition(BaseModel):
    id: int
    title: str
    category: str
    target_rank: str
    actual_rank: str
    competition_date: date

    class Config:
        orm_mode = True
