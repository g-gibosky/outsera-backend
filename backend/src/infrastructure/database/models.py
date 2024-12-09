from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

movie_producer = Table(
    "movie_producer",
    Base.metadata,
    Column(
        "movie_id",
        Integer,
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "producer_id",
        Integer,
        ForeignKey("producers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class MovieModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    title = Column(String)
    studios = Column(String)
    winner = Column(Boolean)

    producers = relationship(
        "ProducerModel", secondary=movie_producer, back_populates="movies"
    )


class ProducerModel(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    movies = relationship(
        "MovieModel", secondary=movie_producer, back_populates="producers"
    )
