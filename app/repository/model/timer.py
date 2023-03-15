from sqlalchemy import Column, Integer, String

from app.repository import Base


class Timer(Base):
    __tablename__ = 'timer'

    id = Column(Integer, primary_key=True)
    expired_at = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
