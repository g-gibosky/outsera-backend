# Movie Awards Analysis Application

An application to analyze movie awards data focusing on producer win patterns. Built with FastAPI, Angular, and SQLite.

## Architecture

The backend follows a hexagonal (ports and adapters) architecture pattern with:
- Domain Layer: Core business logic and entities
- Infrastructure Layer: Database, repositories, and external adapters
- Application Layer: API endpoints and DTOs

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js and npm (for local development)

## Project Setup

1. Clone the repository:
```bash
git clone https://github.com/g-gibosky/outsera-backend
cd movie-awards
```

2. Place your data file:
```bash
# Copy your movielist.csv file to the backend/data directory
cp movielist.csv backend/data/
```

3. Start the application:
```bash
docker-compose up --build
```

The application will be available at:
- Backend: http://localhost:8000

## API Endpoints

### Producers
- GET `/movies/producers/win-intervals`: Get producer win interval

## Project Structure

```
project_root/
├── backend/
│   ├── data/
│   │   └── movielist.csv
│   ├── src/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   ├── application/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
```

## Improvements

1. Data Management
   - Add data validation for CSV imports
   - Don't load everytime the system is reloaded

2. Code Quality
   - Implement stricter type checking
   - Make a single SQL query with the full result
   - Convert SQL query to ORM

## Contact

gibosky@outlook.com
