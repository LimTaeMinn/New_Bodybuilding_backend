from pydantic import BaseModel
from datetime import date

class BodyfatCreate(BaseModel):
    bodyfat_percent: str
    confidence: float
    recommended_diet: str
    recommended_workout: str
    image_url: str

class BodyfatRecord(BaseModel):
    id: int
    bodyfat_percent: str
    confidence: float
    recommended_diet: str
    recommended_workout: str
    image_url: str
    record_date: date

    class Config:
        orm_mode = True
