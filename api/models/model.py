import datetime
import uuid

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, UUID, ForeignKey, Boolean
from sqlalchemy.dialects import postgresql

Base = declarative_base()


class Challenge(Base):
    __tablename__ = "challenge"

    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(length=120), nullable=False, comment="Название челленджа")
    description = Column(String(length=1000))
    user_id = Column(UUID)  # когда модуль будет готов нужно добавить nullable=False)
    date_create = Column(DateTime(timezone=True), default=datetime.datetime.now())
    date_start = Column(DateTime(timezone=True), nullable=False)
    date_end = Column(DateTime(timezone=True), nullable=False)
    status = Column(Boolean, default=True)
    public_challenge = Column(Boolean, default=False)
    day_purposes = relationship("DayPurpose", back_populates="challenge")


class DayPurpose(Base):
    __tablename__ = "day_purpose"

    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(length=120), comment="Название цели на день")
    status = Column(Boolean, default=True)
    date_create = Column(DateTime(timezone=True), default=datetime.datetime.now())
    point = Column(Boolean, default=True, comment="Подтверждение выполнения задачи на день")

    challenge_id = Column(UUID, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="day_purposes")
    day_point = relationship("DayPurposePoint", back_populates="day_purpose")


class DayPurposePoint(Base):
    __tablename__ = "day_purpose_point"

    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(length=120), comment="Название контрольной точки")
    date_start = Column(DateTime(timezone=True), nullable=False)
    date_end = Column(DateTime(timezone=True), nullable=False)
    status = Column(Boolean, default=True, comment="Удаление контрольной точки")
    point = Column(Boolean, default=True, comment="Подтверждение выполнения контрольной точки")

    day_purpose_id = Column(UUID, ForeignKey("day_purpose.id"))
    day_purpose = relationship("DayPurpose", back_populates="day_point")





