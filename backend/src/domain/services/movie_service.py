from typing import Dict
from ..ports.movie_repository import MovieRepository
from ..ports.producer_repository import ProducerRepository
from ...application.config import ProducerIntervalResponse, ProducerInterval

class MovieService:

    def __init__(
        self, movie_repository: MovieRepository, producer_repository: ProducerRepository
    ):
        self._movie_repository = movie_repository
        self._producer_repository = producer_repository

    def get_producer_win_intervals(self) -> ProducerIntervalResponse:
        return ProducerIntervalResponse(
            min=self._producer_repository.get_min_intervals(),
            max=self._producer_repository.get_max_intervals(),
        )
