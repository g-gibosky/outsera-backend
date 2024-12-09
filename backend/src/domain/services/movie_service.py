from typing import List, Optional
from ..models.movie import Movie
from ..ports.movie_repository import MovieRepository

class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self._repository = movie_repository

    def get_all_movies(self) -> List[Movie]:
        return self._repository.find_all()

    def get_movie_by_id(self, id: int) -> Optional[Movie]:
        return self._repository.find_by_id(id)

    def get_movies_by_year(self, year: int) -> List[Movie]:
        return self._repository.find_by_year(year)

    def get_winning_movies(self) -> List[Movie]:
        return self._repository.find_winners()