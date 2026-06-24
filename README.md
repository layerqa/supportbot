# supportbot

🇬🇧 English | [🇷🇺 Русский](README.ru.md)

Telegram bot for support tickets via group threads, built with **aiogram 3**,
**SQLAlchemy 2.0 (async)** and **pydantic-settings**.

## How it works

1. A user writes to the bot in a private chat.
2. The bot creates a forum topic in the support group (`SUPPORT_CHAT_ID`) and
   posts a card as the first message in that topic:
   - the user's name (tap-to-copy),
   - their Telegram ID (tap-to-copy) and a clickable `open chat` link,
   - the `language_code` reported by their client,
   - a `🚫 Ban` button, usable only by admins (`ADMIN_IDS`) and only inside
     the support group.
3. Every following message from the user is mirrored into the topic, and
   every staff reply inside the topic is mirrored back to the user.

The bot talks to the user in Russian or English — either explicitly chosen
via `/language`, or auto-detected from the `language_code` of the Telegram
update.

## Tech stack

- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API framework
- [SQLAlchemy 2.0 (async)](https://docs.sqlalchemy.org/) — ORM / DB access
- [Alembic](https://alembic.sqlalchemy.org/) — DB migrations
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — config from `.env`

## Project structure

```
app/
├── main.py                  # entry point, starts polling
├── config.py                # Settings (pydantic-settings), reads .env
├── logging_config.py        # logging setup
├── i18n.py                   # ru/en translations and locale resolution
├── db/
│   ├── base.py                # DeclarativeBase
│   ├── session.py             # async engine + sessionmaker
│   └── models/                 # SQLAlchemy models (User, Ticket)
├── services/                  # business logic on top of the models
└── bot/
    ├── dispatcher.py          # builds the Dispatcher, routers, middlewares
    ├── middlewares/            # DbSessionMiddleware, etc.
    ├── filters/                 # custom filters (ChatTypeFilter)
    └── handlers/                # start, language (/language), support
                                  # (user <-> ticket flow), group (ticket
                                  # replies + ban button)
migrations/                   # Alembic (async env.py)
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For linting/type-checking, install the dev extras as well:

```bash
pip install -r requirements-dev.txt
```

## Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

| Variable           | Description                                              |
|---------------------|-----------------------------------------------------------|
| `BOT_TOKEN`          | bot token from @BotFather                                  |
| `ADMIN_IDS`          | telegram ids of admins, e.g. `[123, 456]`                  |
| `SUPPORT_CHAT_ID`    | id of the support group (with topics enabled)              |
| `SUPPORT_ORG_NAME`   | organization name used in the welcome message              |
| `DB__*`              | DB connection settings (driver/host/port/user/...)         |

## Database migrations

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Running

```bash
python -m app.main
```

## License

MIT — see [LICENSE](LICENSE).
