from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Notification(Base):
    __table_name__ = "notification"


