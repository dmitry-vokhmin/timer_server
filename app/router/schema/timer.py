from pydantic import BaseModel


class CreateTimerInSchema(BaseModel):
    hours: int
    minutes: int
    seconds: int
    url: str


class CreateTimerOutSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True


class GetTimerSchema(BaseModel):
    id: int
    time_left: int
