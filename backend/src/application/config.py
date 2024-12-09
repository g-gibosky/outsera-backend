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