from pydantic import BaseModel
from datetime import datetime


class EDFDataCreate(BaseModel):
    filename: str
    channel_count: int
    sampling_freq: float
    duration: float
    timestamp: datetime


class EDFDataResponse(EDFDataCreate):
    id: int

    class Config:
        orm_mode = True
