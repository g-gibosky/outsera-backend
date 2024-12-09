from dataclasses import dataclass
from typing import Optional

@dataclass
class Producer:
    id: Optional[int]
    name: str

@dataclass
class MovieProducer:
    movie_id: int
    producer_id: int