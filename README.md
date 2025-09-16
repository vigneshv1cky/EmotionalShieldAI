# EmotionalShieldAI

EmotionalShieldAI is a FastAPI-based backend application designed to provide emotional well-being support and analysis. It leverages modern Python libraries and a SQLite database to manage and process user data securely and efficiently.

## Features

- RESTful API built with FastAPI
- SQLite database integration
- Modular code structure (CRUD, models, schemas, utils)
- Docker Compose support for easy deployment
- Environment management with `env_emotionalshieldai` virtual environment

## Project Structure

```
EmotionalShieldAI/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── requirements.txt
├── compose.yml
├── tradefit.db
├── env_emotionalshieldai/
└── ...
```

## Getting Started

### Prerequisites

- Python 3.13+
- [pip](https://pip.pypa.io/en/stable/)
- (Optional) [Docker](https://www.docker.com/)

### Setup (Local)

1. **Clone the repository:**

   ```bash
   git clone <repo-url>
   cd EmotionalShieldAI
   ```

2. **Create and activate virtual environment:**

   ```bash
   python3 -m venv env_emotionalshieldai
   source env_emotionalshieldai/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Access the API docs:**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

### Setup (Docker)

1. **Build and run with Docker Compose:**

   ```bash
   docker compose up --build
   ```

## API Documentation

Interactive API documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

## Database

- Default database: `tradefit.db` (SQLite)
- Database models and CRUD operations are defined in `app/models.py` and `app/crud.py`.

## Testing

- Use tools like [Postman](https://www.postman.com/) or the included `TradeFit.postman_collection.json` to test API endpoints.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
