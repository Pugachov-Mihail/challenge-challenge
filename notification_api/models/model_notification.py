import datetime

from pydantic import BaseModel


class Notification(BaseModel):
    day_week: int
    periodicity: int
    period: int
    time_start: str
    time_end: str


