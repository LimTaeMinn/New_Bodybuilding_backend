from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from models.bodyfat import BodyfatHistory


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    competition_histories = relationship("CompetitionHistory", back_populates="user")


    routines = relationship("models.routine.WorkoutRoutine", back_populates="user")
    
    # ✅ 추가된 필드
    name = Column(String)
    phone_number = Column(String)

    bodyfat_histories = relationship("models.bodyfat.BodyfatHistory", back_populates="user")


    # ✅ [1단계] 프로필 이미지 경로 추가
    profile_image_url = Column(String, nullable=True)