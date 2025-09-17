# Morning TradeFit Scan API

Morning TradeFit Scan API is a FastAPI-based backend application designed to provide emotional well-being support and analysis. It leverages modern Python libraries and a SQLite database to manage and process user data securely and efficiently.

## Features

- RESTful API built with FastAPI
- SQLite database integration
- Modular code structure (CRUD, models, schemas, utils)
- Docker Compose support for easy deployment

## Project Structure

```

EmotionalShieldAI/
├── .env
├── .git/
├── .gitignore
├── README.md
├── TradeFit.postman_collection.json
├── __pycache__/
├── app/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── compose.yml
├── env_emotionalshieldai/
│   ├── .gitignore
│   ├── bin/
│   ├── include/
│   ├── lib/
│   └── pyvenv.cfg
├── requirements.txt
├── run.sh
├── sqlite_to_mysql.md
└── tradefit.db

```

## Getting Started

### Prerequisites

- Python 3.13+
- [pip](https://pip.pypa.io/en/stable/)
- (Optional) [Docker](https://www.docker.com/)

### Setup (Local)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vigneshv1cky/EmotionalShieldAI.git
   cd EmotionalShieldAI
   ```

2. **Run the application using the provided script:**

   ```bash
   ./run.sh
   ```

   - The script will automatically create a virtual environment (if not present), install dependencies, and start the FastAPI server.

3. **Access the API docs:**
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
