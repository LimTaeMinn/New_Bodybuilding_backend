from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import date

class CompetitionHistory(Base):
    __tablename__ = "competition_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    category = Column(String)
    target_rank = Column(String)
    actual_rank = Column(String)
    competition_date = Column(Date, default=date.today)

    # User와 관계 설정 (auth/models.py의 User에 연결될 예정)
    user = relationship("User", back_populates="competition_histories")
