from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..infrastructure.database.connection import get_db
from ..domain.services.movie_service import MovieService
from ..infrastructure.repositories.sqlalchemy_movie_repository import SqlAlchemyMovieRepository
from ..infrastructure.repositories.sqlalchemy_producer_repository import SqlAlchemyProducerRepository
from .config import ProducerIntervalResponse

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)


def get_movie_service(db: Session = Depends(get_db)):
    movie_repository = SqlAlchemyMovieRepository(db)
    producer_repository = SqlAlchemyProducerRepository(db)
    return MovieService(movie_repository, producer_repository)


@router.get("/producers/win-intervals", response_model=ProducerIntervalResponse)
def get_producer_win_intervals(
    movie_service: MovieService = Depends(get_movie_service),
) -> ProducerIntervalResponse:
    return movie_service.get_producer_win_intervals()


movie_router = router
