from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import date

class BodyfatHistory(Base):
    __tablename__ = "bodyfat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bodyfat_percent = Column(String)
    confidence = Column(Float)
    recommended_diet = Column(String)
    recommended_workout = Column(String)
    image_url = Column(String)
    record_date = Column(Date, default=date.today)

    user = relationship("auth.models.User", back_populates="bodyfat_histories")
