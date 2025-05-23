# schemas/routine.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WorkoutItemBase(BaseModel):
    name: str
    count: int

class WorkoutItemCreate(WorkoutItemBase):
    pass

class WorkoutItem(WorkoutItemBase):
    id: int

    model_config = {
        "from_attributes": True  # ✅ 필수!
    }


class WorkoutRoutineBase(BaseModel):
    title: str

class WorkoutRoutineCreate(WorkoutRoutineBase):
    items: List[WorkoutItemCreate]

class WorkoutRoutine(WorkoutRoutineBase):
    id: int
    created_at: datetime
    items: List[WorkoutItem]

    model_config = {
        "from_attributes": True  # ✅ 필수!
    }
