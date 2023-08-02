import uuid

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, UUID, ForeignKey, Integer, Time
from sqlalchemy.dialects import postgresql

from api.models.model_challenge import Challenge
from api.models.types import Choise

Base = declarative_base()


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

    challenge_id = Column(UUID, ForeignKey(Challenge.id))
    challenge = relationship(Challenge, back_populates="challenge")
