from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.database.connection import db, get_db
from infrastructure.adapters.csv_loader import CsvLoader
from infrastructure.repositories.sqlalchemy_movie_repository import SqlAlchemyMovieRepository
from application.routers import movie_router
from sqlalchemy.orm import Session

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movie_router.router)

# Application startup
@app.on_event("startup")
async def startup_event():
    db.create_database()
    session = get_db()
    try:
        repository = SqlAlchemyMovieRepository(session)
        if len(repository.find_all()) == 0:
            movies = CsvLoader.load_movies("./data/movielist.csv")
            for movie in movies:
                repository.save(movie)
            print("Initial data loaded successfully!")
    finally:
        session.close()