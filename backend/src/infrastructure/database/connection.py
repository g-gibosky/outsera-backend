from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base
from typing import Generator


class Database:
    def __init__(self, url: str = "sqlite:///./movies.db"):
        self.engine = create_engine(url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_database(self):
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
            
db = Database()
def get_db():
    return next(db.get_session())
