from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.infrastructure.database.models import MovieModel, ProducerModel
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
import pandas as pd
from .context import sys, os
from src.infrastructure.database.models import MovieModel, ProducerModel
from src.infrastructure.repositories.sqlalchemy_movie_repository import (
    SqlAlchemyMovieRepository,
)
from src.infrastructure.repositories.sqlalchemy_producer_repository import (
    SqlAlchemyProducerRepository,
)


def create_test_data(session: Session):
    test_data = [
        {
            "producer": "Producer A",
            "movies": [
                {"year": 2000, "winner": True},
                {"year": 2002, "winner": True},
                {"year": 2015, "winner": True},
            ],
        },
        {
            "producer": "Producer B",
            "movies": [
                {"year": 2005, "winner": True},
                {"year": 2006, "winner": True},
                {"year": 2025, "winner": True},
            ],
        },
    ]

    producer_map = {}
    for producer_data in test_data:
        producer = ProducerModel(name=producer_data["producer"])
        session.add(producer)
        session.flush()
        producer_map[producer.name] = producer

        for movie_data in producer_data["movies"]:
            movie = MovieModel(
                year=movie_data["year"],
                title=f"Movie {movie_data['year']}",
                studios="Test Studio",
                winner=movie_data["winner"],
            )
            session.add(movie)
            session.flush()
            movie.producers.append(producer)

    session.commit()


def test_get_producer_win_intervals(test_db):
    client, session = test_db

    create_test_data(session)

    response = client.get("/movies/producers/win-intervals")

    assert response.status_code == 200

    data = response.json()
    assert "min" in data
    assert "max" in data

    min_intervals = data["min"]
    assert len(min_intervals) > 0
    assert min_intervals[0]["producer"] == "Producer B"
    assert min_intervals[0]["interval"] == 1
    assert min_intervals[0]["previousWin"] == 2005
    assert min_intervals[0]["followingWin"] == 2006

    max_intervals = data["max"]
    assert len(max_intervals) > 0
    assert max_intervals[0]["producer"] == "Producer B"
    assert max_intervals[0]["interval"] == 19
    assert max_intervals[0]["previousWin"] == 2006
    assert max_intervals[0]["followingWin"] == 2025


def test_empty_database(test_db):
    client, session = test_db

    response = client.get("/movies/producers/win-intervals")

    assert response.status_code == 200

    data = response.json()
    assert "min" in data
    assert "max" in data
    assert len(data["min"]) == 0
    assert len(data["max"]) == 0


def test_single_win_producers(test_db):
    client, session = test_db

    producer = ProducerModel(name="Single Win Producer")
    session.add(producer)

    movie = MovieModel(
        year=2000, title="Single Win Movie", studios="Test Studio", winner=True
    )
    movie.producers.append(producer)
    session.add(movie)
    session.commit()

    response = client.get("/movies/producers/win-intervals")

    data = response.json()
    assert len(data["min"]) == 0
    assert len(data["max"]) == 0


def test_non_winning_movies(test_db):
    client, session = test_db

    producer = ProducerModel(name="Non Winner Producer")
    session.add(producer)

    movie1 = MovieModel(
        year=2000, title="Non Win Movie 1", studios="Test Studio", winner=False
    )
    movie2 = MovieModel(
        year=2001, title="Non Win Movie 2", studios="Test Studio", winner=False
    )

    movie1.producers.append(producer)
    movie2.producers.append(producer)

    session.add(movie1)
    session.add(movie2)
    session.commit()

    response = client.get("/movies/producers/win-intervals")

    data = response.json()
    assert len(data["min"]) == 0
    assert len(data["max"]) == 0
