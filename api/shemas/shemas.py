import uuid

from datetime import datetime
from pydantic import BaseModel, validator
from fastapi.exceptions import HTTPException


class DayPurposePoint(BaseModel):
    title: str
    date_start: datetime
    date_end: datetime
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
    title: str
    description: str
    date_start: datetime
    date_end: datetime
    day_purposes: list[DayPurpose]

    class Config:
        orm_mode = True


class CreateChallenge(BaseModel):
    title: str
    description: str
    date_start: datetime
    date_end: datetime

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
