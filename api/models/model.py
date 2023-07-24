from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Challenge(Base):
    __tablename__ = "challenge"