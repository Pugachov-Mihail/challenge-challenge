from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, Integer, Column, Text

Base = declarative_base()


class Challenge(Base):
    __tablename__ = "challenge"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    
