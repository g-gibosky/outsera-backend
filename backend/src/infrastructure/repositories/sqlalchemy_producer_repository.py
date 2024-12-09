from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...application.config import ProducerInterval
from ...domain.models.producer import Producer
from ...domain.ports.producer_repository import ProducerRepository
from ..database.models import ProducerModel


class SqlAlchemyProducerRepository(ProducerRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, producer: Producer) -> Producer:
        db_producer = ProducerModel(name=producer.name)
        self._session.add(db_producer)
        self._session.commit()
        self._session.refresh(db_producer)
        return self._convert_to_domain(db_producer)
    
    def get_min_intervals(self) -> List[ProducerInterval]:
        query = text(
            """
            WITH consecutive_wins AS (
                SELECT 
                    p.name as producer,
                    m.year as win_year,
                    LEAD(m.year) OVER (PARTITION BY p.name ORDER BY m.year) as next_win,
                    LEAD(m.year) OVER (PARTITION BY p.name ORDER BY m.year) - m.year as interval
                FROM producers p
                JOIN movie_producer mp ON p.id = mp.producer_id
                JOIN movies m ON mp.movie_id = m.id
                WHERE m.winner = 1
            ),
            min_interval AS (
                SELECT MIN(interval) as min_interval
                FROM consecutive_wins 
                WHERE interval IS NOT NULL
            )
            SELECT producer, interval, win_year as previousWin, next_win as followingWin
            FROM consecutive_wins, min_interval
            WHERE interval IS NOT NULL
            AND interval = min_interval
            ORDER BY producer, win_year;
        """
        )

        result = self._session.execute(query)
        return [
            ProducerInterval(
                producer=row.producer,
                interval=row.interval,
                previousWin=row.previousWin,
                followingWin=row.followingWin,
            )
            for row in result.fetchall()
        ]

    def get_max_intervals(self) -> List[ProducerInterval]:
        query = text(
            """
            WITH consecutive_wins AS (
                SELECT 
                    p.name as producer,
                    m.year as win_year,
                    LEAD(m.year) OVER (PARTITION BY p.name ORDER BY m.year) as next_win,
                    LEAD(m.year) OVER (PARTITION BY p.name ORDER BY m.year) - m.year as interval
                FROM producers p
                JOIN movie_producer mp ON p.id = mp.producer_id
                JOIN movies m ON mp.movie_id = m.id
                WHERE m.winner = 1
            ),
            max_interval AS (
                SELECT MAX(interval) as max_interval
                FROM consecutive_wins 
                WHERE interval IS NOT NULL
            )
            SELECT producer, interval, win_year as previousWin, next_win as followingWin
            FROM consecutive_wins, max_interval
            WHERE interval IS NOT NULL
            AND interval = max_interval
            ORDER BY producer, win_year;
        """
        )

        result = self._session.execute(query)
        return [
            ProducerInterval(
                producer=row.producer,
                interval=row.interval,
                previousWin=row.previousWin,
                followingWin=row.followingWin,
            )
            for row in result.fetchall()
        ]

    def _convert_to_domain(self, db_producer: ProducerModel) -> Producer:
        return Producer(id=db_producer.id, name=db_producer.name)
