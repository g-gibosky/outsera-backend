from dataclasses import dataclass
from typing import List
from .producer import Producer

@dataclass
class Movie:
    id: int
    year: int
    title: str
    studios: str
    winner: bool
    producers: List[Producer] = None