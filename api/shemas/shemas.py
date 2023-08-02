import uuid

from datetime import datetime, time
from pydantic import BaseModel, validator
from fastapi.exceptions import HTTPException


class DayPurposePoint(BaseModel):
    title: str
    date_start: time
    date_end: time
    point: bool

    @validator("title")
    def validate_title(cls, value):
        if len(value) > 120:
            raise HTTPException(
                status_code=400,
                detail="Длинное название"
            )
        return value

    class Config:
        orm_mode = True


class DayPurpose(BaseModel):
    title: str
    point: bool


    @validator("title")
    def validate_title(cls, value):
        if len(value) > 120:
            raise HTTPException(
                status_code=400,
                detail="Длинное название"
            )
        return value

    class Config:
        orm_mode = True


class DayPurposeCreate(DayPurpose):
    challenge_id: uuid.UUID


class Challenge(BaseModel):
    user_id: uuid.UUID
    title: str
    description: str
    date_start: datetime
    date_end: datetime
    day_purposes: list[DayPurpose]
    day_point: list[DayPurposePoint]

    class Config:
        orm_mode = True


class SettingChallenge(BaseModel):
    type: int
    paid: bool = False
    cost: float
    limitations: bool = False
    count_users: int

    class Config:
        orm_mode = True


class CreateChallenge(BaseModel):
    title: str
    description: str
    date_start: datetime
    date_end: datetime
    user_id: uuid.UUID

    @validator("description")
    def validate_description(cls, value):
        if len(value) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Длинное описание"
            )
        return value

    @validator("title")
    def validate_title(cls, value):
        if len(value) > 120:
            raise HTTPException(
                status_code=400,
                detail="Длинное название"
            )
        return value


class Notification(BaseModel):
    day_week: int
    periodicity: int
    period: int
    time_start: time
    time_end: time
