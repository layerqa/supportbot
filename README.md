# supportbot
Telegram bot for support tickets via telegram group treads

## Стек

- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API framework
- [SQLAlchemy 2.0 (async)](https://docs.sqlalchemy.org/) — ORM/доступ к БД
- [Alembic](https://alembic.sqlalchemy.org/) — миграции БД
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — конфиг из `.env`

## Структура проекта

```
app/
├── main.py                  # точка входа, запуск polling
├── config.py                # Settings (pydantic-settings), читает .env
├── logging_config.py        # настройка логирования
├── db/
│   ├── base.py               # DeclarativeBase
│   ├── session.py            # async engine + sessionmaker
│   └── models/                # SQLAlchemy-модели (User, Ticket)
├── services/                 # бизнес-логика над моделями
└── bot/
    ├── dispatcher.py         # сборка Dispatcher, роутеров и мидлварей
    ├── middlewares/           # DbSessionMiddleware и т.п.
    ├── filters/                # кастомные фильтры (ChatTypeFilter)
    └── handlers/               # хендлеры: start, support (диалог с юзером),
                                 # group (ответы поддержки в топиках)
migrations/                  # alembic (async env.py)
```

Идея бота: сообщение пользователя в приватном чате создаёт тикет и форум-топик
в группе поддержки (`SUPPORT_CHAT_ID`); дальнейшая переписка зеркалируется
между пользователем и соответствующим топиком.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Конфигурация

Скопируйте `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

| Переменная        | Описание                                              |
|--------------------|--------------------------------------------------------|
| `BOT_TOKEN`         | токен бота от @BotFather                                |
| `ADMIN_IDS`         | список telegram id админов, формат `[123, 456]`        |
| `SUPPORT_CHAT_ID`   | id группы поддержки (с включёнными топиками)            |
| `DB__*`             | параметры подключения к БД (driver/host/port/user/...)  |

## Миграции БД

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Запуск

```bash
python -m app.main
```
