from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .infrastructure.database.connection import db, get_db
from .infrastructure.adapters.data_loader import CsvLoader
from .infrastructure.repositories.sqlalchemy_movie_repository import SqlAlchemyMovieRepository
from .infrastructure.repositories.sqlalchemy_producer_repository import SqlAlchemyProducerRepository
from .application.routers_movies import router as movie_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movie_router)


@app.on_event("startup")
async def startup_event():
    print("Starting database initialization...")
    db.create_database()  # This will now drop and recreate all tables
    session = get_db()
    try:
        movie_repository = SqlAlchemyMovieRepository(session)
        producer_repository = SqlAlchemyProducerRepository(session)

        print("Loading data from CSV...")
        movies, producers = CsvLoader.load_movies("movielist.csv")

        print(f"Found {len(producers)} unique producers")
        # First save all producers and create a mapping
        producer_map = {}
        for producer in producers:
            saved_producer = producer_repository.save(producer)
            producer_map[saved_producer.name] = saved_producer

        print(f"Saved {len(producer_map)} producers")
        print("Saving movies and their associations...")

        # Then save movies with their producers
        for movie in movies:
            saved_movie = movie_repository.save(movie)

            # Add producers to the movie
            for producer_name in movie.producer_names:
                if producer_name in producer_map:
                    movie_repository.add_producer(
                        saved_movie.id, producer_map[producer_name].id
                    )

        print("Initial data loaded successfully!")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise
    finally:
        session.close()
