import datetime
import uuid

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Time, UUID, ForeignKey, Boolean, Integer, Float, DateTime
from sqlalchemy.dialects import postgresql


from api.models.types import Choise


Base = declarative_base()


class Challenge(Base):
    __tablename__ = "challenge"

    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(length=120), nullable=False, comment="Название челленджа")
    description = Column(String(length=1000))
    user_id = Column(UUID,
                     comment="Пользователь который создал челлендж")  # когда модуль будет готов нужно добавить nullable=False)
    date_create = Column(DateTime(timezone=True), default=datetime.datetime.now())
    date_update = Column(DateTime(timezone=True))
    date_start = Column(DateTime(timezone=True), nullable=False)
    date_end = Column(DateTime(timezone=True), nullable=False)
    status = Column(Boolean, default=True)
    public_challenge = Column(Boolean, default=False)

    day_purposes = relationship("DayPurpose", back_populates="challenge", cascade="delete, all")
    setting_challenge = relationship("SettingChallenge", back_populates="challenge", cascade="delete, all")
    count_user = relationship("CountUser", back_populates="challenge", cascade="delete, all")
    day_point = relationship("DayPurposePoint", back_populates="challenge", cascade="delete, all")
    notification = relationship("Notification", back_populates="challenge", cascade="delete, all")


class DayPurpose(Base):
    __tablename__ = "day_purpose"

    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(length=120), comment="Название цели на день")
    status = Column(Boolean, default=True)
    date_create = Column(DateTime(timezone=True), default=datetime.datetime.now())
    date_update = Column(DateTime(timezone=True))
    point = Column(Boolean, default=True, comment="Подтверждение выполнения задачи на день")

    challenge_id = Column(UUID, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="day_purposes")
    day_point = relationship("DayPurposePoint", back_populates="day_purpose")


class DayPurposePoint(Base):
    __tablename__ = "day_purpose_point"

    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(length=120), comment="Название контрольной точки")
    date_start = Column(Time(timezone=True), nullable=False)
    date_end = Column(Time(timezone=True), nullable=False)
    status = Column(Boolean, default=True, comment="Удаление контрольной точки")
    point = Column(Boolean, default=True, comment="Подтверждение выполнения контрольной точки")
    date_update = Column(DateTime(timezone=True))
    date_create = Column(DateTime(timezone=True), default=datetime.datetime.now())

    day_purpose_id = Column(UUID, ForeignKey("day_purpose.id"))
    challenge_id = Column(UUID, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="day_point")
    day_purpose = relationship("DayPurpose", back_populates="day_point")


class SettingChallenge(Base):
    __tablename__ = "setting_challenge"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Choise({
        0: "Индивидуальный",
        1: "Групповой"
    }), default=0)
    paid = Column(Boolean, default=False)
    cost = Column(Float)
    limitations = Column(Boolean, default=False)
    count_users = Column(Integer)
    status = Column(Boolean, default=True)

    challenge_id = Column(UUID, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="setting_challenge")


class CountUser(Base):
    __tablename__ = "count_user"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True)
    users_list = Column(UUID)
    status = Column(Boolean, default=True)
    send_event = Column(UUID)
    activate_invite = Column(Boolean, default=False)

    challenge_id = Column(UUID, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="count_user")


class Notification(Base):
    __tablename__ = "notification"

    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    day_week = Column(Integer, nullable=False)
    periodicity = Column(Choise({
        0: "Раз в час",
        1: "Раз в день"
    }))
    period = Column(Integer, default=0) # 0 - всегда, 1-будни, 2-выходные
    time_start = Column(Time)
    time_end = Column(Time)

    challenge_id = Column(UUID, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="notification")
