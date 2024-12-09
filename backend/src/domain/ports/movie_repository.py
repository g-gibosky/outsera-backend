from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.movie import Movie

class MovieRepository(ABC):
    @abstractmethod
    def save(self, movie: Movie) -> Movie:
        pass

    @abstractmethod
    def find_all(self) -> List[Movie]:
        pass