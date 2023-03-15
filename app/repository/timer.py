from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import insert, select

from app.repository import get_db
from app.repository.model.timer import Timer


class TimerRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_timer(self, url: str, time: int) -> Timer:
        query = self.session.scalars(
            insert(Timer).returning(Timer)
            .values(url=url, expired_at=time)
        )
        return query.first()

    def get_timer(self, timer_id: int) -> Timer:
        query = select(Timer).where(Timer.id == timer_id)
        return self.session.scalars(query).first()


def get_timer_repository(session=Depends(get_db)):
    return TimerRepository(session)
