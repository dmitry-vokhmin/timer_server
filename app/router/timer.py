from fastapi import APIRouter, Depends

from app.router.schema.timer import (
    CreateTimerInSchema,
    CreateTimerOutSchema,
    GetTimerSchema
)
from app.service.timer import TimerService, get_timer_service

router = APIRouter()


@router.post('/timers', response_model=CreateTimerOutSchema)
def create_timer(
        timer_schema: CreateTimerInSchema,
        timer_service: TimerService = Depends(get_timer_service)
) -> CreateTimerOutSchema:
    return timer_service.create_timer(timer_schema)


@router.get('/timers/{timer_id}', response_model=GetTimerSchema)
def get_timer(
        timer_id: int,
        timer_service: TimerService = Depends(get_timer_service)
) -> GetTimerSchema:
    return timer_service.get_timer(timer_id)
