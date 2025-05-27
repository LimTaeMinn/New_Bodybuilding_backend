# models/routine.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class WorkoutRoutine(Base):
    __tablename__ = "workout_routines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="routines")
    items = relationship("WorkoutItem", back_populates="routine", cascade="all, delete")

class WorkoutItem(Base):
    __tablename__ = "workout_items"

    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("workout_routines.id"))
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)

    routine = relationship("WorkoutRoutine", back_populates="items", lazy="noload")


