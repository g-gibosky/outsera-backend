from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.models.movie import Movie
from ...domain.models.producer import Producer
from ...domain.ports.movie_repository import MovieRepository
from ..database.models import MovieModel, ProducerModel


class SqlAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, movie: Movie) -> Movie:
        db_movie = MovieModel(
            year=movie.year,
            title=movie.title,
            studios=movie.studios,
            winner=movie.winner,
        )
        self._session.add(db_movie)
        self._session.commit()
        self._session.refresh(db_movie)
        return self._convert_to_domain(db_movie)

    def add_producer(self, movie_id: int, producer_id: int):
        movie = (
            self._session.query(MovieModel).filter(MovieModel.id == movie_id).first()
        )
        producer = (
            self._session.query(ProducerModel)
            .filter(ProducerModel.id == producer_id)
            .first()
        )

        if movie and producer and producer not in movie.producers:
            movie.producers.append(producer)
            self._session.commit()

    def find_all(self) -> List[Movie]:
        db_movies = self._session.query(MovieModel).all()
        return [self._convert_to_domain(db_movie) for db_movie in db_movies]

    def find_by_id(self, id: int) -> Optional[Movie]:
        db_movie = self._session.query(MovieModel).filter(MovieModel.id == id).first()
        return self._convert_to_domain(db_movie) if db_movie else None

    def _convert_to_domain(self, db_movie: MovieModel) -> Movie:
        producers = (
            [Producer(id=p.id, name=p.name) for p in db_movie.producers]
            if db_movie.producers
            else []
        )

        return Movie(
            id=db_movie.id,
            year=db_movie.year,
            title=db_movie.title,
            studios=db_movie.studios,
            winner=db_movie.winner,
            producers=producers,
        )
