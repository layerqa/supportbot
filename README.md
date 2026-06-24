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
deploy/
└── supportbot.service        # systemd unit file
Dockerfile                    # container image for the bot
docker-compose.yml            # bot + postgres for local/server deployment
entrypoint.sh                 # runs migrations, then starts the bot
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

## Deployment

### Docker Compose

Builds the bot image and runs it alongside a Postgres 16 container.

```bash
cp .env.example .env
# edit .env with your values
docker compose up -d --build
```

The bot container's `entrypoint.sh` runs `alembic upgrade head` automatically
before starting the bot, so migrations are applied on every deploy.
`docker-compose.yml` overrides `DB__HOST`/`DB__PORT` to point at the bundled
`db` service — the rest of the database settings (`DB__USER`, `DB__PASSWORD`,
`DB__NAME`) are read from the same `.env` file and used to initialize the
Postgres container too.

### systemd

For a bare-metal/VM deployment without Docker:

```bash
sudo mkdir -p /opt/supportbot
sudo cp -r . /opt/supportbot
cd /opt/supportbot

python -m venv .venv
.venv/bin/pip install -r requirements.txt

cp .env.example .env
# edit .env with your values

sudo useradd --system --shell /usr/sbin/nologin supportbot
sudo chown -R supportbot:supportbot /opt/supportbot

sudo cp deploy/supportbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now supportbot
```

The unit file runs `alembic upgrade head` before every start
(`ExecStartPre`) and restarts the bot on failure. It assumes the app lives
in `/opt/supportbot` and runs as the `supportbot` user — edit `User=`,
`WorkingDirectory=` and the venv paths in `deploy/supportbot.service` if your
setup differs.

```bash
journalctl -u supportbot -f   # view logs
```

## License

MIT — see [LICENSE](LICENSE).
