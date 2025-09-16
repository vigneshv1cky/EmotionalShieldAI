# Migrating from SQLite to PostgreSQL

This guide explains how to convert your SQLite database to PostgreSQL for your FastAPI project.

---

## 1. Install PostgreSQL Driver

Add `psycopg2-binary` to your `requirements.txt`:

```
psycopg2-binary
```

Then install it:

```bash
pip install -r requirements.txt
```

---

## 2. Update Database URL in `app/config.py`

Replace your SQLite URL with a PostgreSQL URL:

```
# Example for config.py
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/yourdbname"
```

---

## 3. Update `app/database.py` to Use the New URL

Make sure your SQLAlchemy engine uses the PostgreSQL URL.

---

## 4. Create the PostgreSQL Database

```bash
# In psql or using a GUI like pgAdmin
CREATE DATABASE yourdbname;
```

---

## 5. Migrate Data from SQLite to PostgreSQL

You can use the `pgloader` tool for a direct migration:

### Install pgloader

On macOS:

```bash
brew install pgloader
```

### Run Migration

```bash
pgloader sqlite:///absolute/path/to/tradefit.db postgresql://username:password@localhost/yourdbname
```

---

## 6. Apply Migrations (if using Alembic or similar)

If you use Alembic, run:

```bash
alembic upgrade head
```

---

## 7. Update Docker Compose (if using Docker)

Update your `compose.yml` to add a PostgreSQL service:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: username
      POSTGRES_PASSWORD: password
      POSTGRES_DB: yourdbname
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 8. Test Your App

Update your `.env` or config to point to PostgreSQL and restart your app.

---

Let me know if you want the exact code changes for your `app/database.py` or help with any step!
