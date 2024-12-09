from typing import List
from pydantic import BaseModel

class MovieResponse(BaseModel):
    id: int
    year: int
    title: str
    studios: str
    producers: str
    winner: bool

    class Config:
        orm_mode = True


class ProducerInterval(BaseModel):
    producer: str
    interval: int
    previousWin: int
    followingWin: int


class ProducerIntervalResponse(BaseModel):
    min: List[ProducerInterval]
    max: List[ProducerInterval]
