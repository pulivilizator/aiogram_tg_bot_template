# **Telegram Bot Template on Aiogram**

---

A template for a Telegram bot that includes:
- working with a cache (Redis),
- a database (PostgreSQL, SQLAlchemy),
- localization (Fluentogram),
- a message broker (NATS),
- Alembic migrations,
- and the bot logic itself on [Aiogram](https://docs.aiogram.dev/).

You can find the full list of dependencies in [`pyproject.toml`](./pyproject.toml).

---

## Local Launch

1. Clone the project.
2. Rename the file [`secrets.toml.example`](secrets.toml.example) to `.secrets.toml` and specify your bot token in it.
3. Start the project with the command:
   ```bash
   docker compose --profile=all up
    ```
4. The bot has a single /start command for testing.

---

## Structure

```
├── bot
│   ├── cache             # Cache
│   ├── core              # Core parts of the bot
│   │   ├── middlewares   # All middlewares (logger, i18n, registration, etc.)
│   │   ├── providers     # Dependency injection providers (dishka)
│   │   ├── dto.py        # Pydantic models for DTO
│   │   └── enums.py      # Enums
│   ├── handling          # Logic for processing incoming messages
│   │   ├── dialogs       # Windows and dialogs (aiogram_dialog)
│   │   ├── filters       # Custom aiogram filters
│   │   ├── handlers      # Aiogram handlers
│   │   ├── states        # FSM states
│   │   └── utils         # Utility functions
│   ├── interactors       # Business logic
│   ├── nats_storage      # State storage on NATS
│   ├── repository        # Repositories for database operations
│   └── __main__.py       # Bot entry point
├── config                # Common application configs (Dynaconf, Pydantic)
├── database
│   ├── config            # Database config
│   ├── migrations        # Alembic migrations
│   └── models            # SQLAlchemy models
├── i18n                  # Files for internationalization
├── logs                  # Logging configuration
├── nats                  # NATS configuration and migrations
├── secrets.toml.example  # Secrets template
├── app.py                # Entry point
├── docker-compose.yaml   # Docker Compose configuration
├── alembic.ini           # Alembic configuration
└── pyproject.toml        # Dependencies (uv)
```