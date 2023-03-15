from time import time

from fastapi import Depends

from app.repository.model.timer import Timer
from app.repository.timer import TimerRepository, get_timer_repository
from app.router.schema.timer import CreateTimerInSchema, GetTimerSchema


class TimerService:
    def __init__(self, repository: TimerRepository):
        self.repository = repository

    def create_timer(self, timer_schema: CreateTimerInSchema) -> Timer:
        expired_at = int(time() + self.get_seconds(timer_schema))
        return self.repository.create_timer(timer_schema.url, expired_at)

    def get_timer(self, timer_id: int) -> GetTimerSchema:
        timer = self.repository.get_timer(timer_id)
        time_left = timer.expired_at - time()
        if time_left < 0:
            time_left = 0
        return GetTimerSchema(id=timer.id, time_left=time_left)

    def get_seconds(self, timer_schema: CreateTimerInSchema):
        return (timer_schema.hours * 3600
                + timer_schema.minutes * 60
                + timer_schema.seconds)


def get_timer_service(timer_repository=Depends(get_timer_repository)):
    return TimerService(timer_repository)
