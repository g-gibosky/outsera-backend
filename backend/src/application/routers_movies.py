from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..infrastructure.database.connection import get_db
from ..domain.services.movie_service import MovieService
from ..infrastructure.repositories.sqlalchemy_movie_repository import SqlAlchemyMovieRepository
from .config import MovieResponse

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

def get_movie_service(db: Session = Depends(get_db)):
    repository = SqlAlchemyMovieRepository(db)
    return MovieService(repository)

@router.get("", response_model=List[MovieResponse])
def get_movies(
    movie_service: MovieService = Depends(get_movie_service)
):
    return movie_service.get_all_movies()

movie_router = router