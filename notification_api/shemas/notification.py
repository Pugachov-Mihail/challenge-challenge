import uuid
from datetime import time

from pydantic import BaseModel


class Challenge(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        orm_mode = True


class Notification(BaseModel):
    day_week: int
    periodicity: int
    period: int
    time_start: time
    time_end: time
    challenge: Challenge

    class Config:
        orm_mode = True
