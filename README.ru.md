# supportbot

[🇬🇧 English](README.md) | 🇷🇺 Русский

Telegram-бот для тикетов поддержки через топики группы, на **aiogram 3**,
**SQLAlchemy 2.0 (async)** и **pydantic-settings**.

## Как это работает

1. Пользователь пишет боту в приватном чате.
2. Бот создаёт форум-топик в группе поддержки (`SUPPORT_CHAT_ID`) и
   отправляет туда первым сообщением карточку:
   - имя пользователя (копируется по тапу),
   - его Telegram ID (копируется по тапу) и кликабельная ссылка `open chat`,
   - `language_code`, который сообщает клиент пользователя,
   - кнопку `🚫 Забанить` — доступна только админам (`ADMIN_IDS`) и только
     внутри группы поддержки.
3. Каждое следующее сообщение пользователя зеркалируется в этот топик, а
   каждый ответ поддержки в топике — обратно пользователю.

Бот отвечает пользователю на русском или английском — язык можно явно
выбрать через `/language`, либо он определяется автоматически по
`language_code` Telegram-апдейта.

## Стек

- [aiogram 3](https://docs.aiogram.dev/) — фреймворк для Telegram Bot API
- [SQLAlchemy 2.0 (async)](https://docs.sqlalchemy.org/) — ORM / доступ к БД
- [Alembic](https://alembic.sqlalchemy.org/) — миграции БД
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — конфиг из `.env`

## Структура проекта

```
app/
├── main.py                  # точка входа, запуск polling
├── config.py                # Settings (pydantic-settings), читает .env
├── logging_config.py        # настройка логирования
├── i18n.py                   # переводы ru/en и определение локали
├── db/
│   ├── base.py                # DeclarativeBase
│   ├── session.py             # async engine + sessionmaker
│   └── models/                 # SQLAlchemy-модели (User, Ticket)
├── services/                  # бизнес-логика над моделями
└── bot/
    ├── dispatcher.py          # сборка Dispatcher, роутеров и мидлварей
    ├── middlewares/            # DbSessionMiddleware и т.п.
    ├── filters/                 # кастомные фильтры (ChatTypeFilter)
    └── handlers/                 # start, language (/language), support
                                   # (диалог с юзером), group (ответы
                                   # поддержки в топиках + кнопка бана)
migrations/                   # alembic (async env.py)
```

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Для линтера/тайпчекера установите ещё dev-зависимости:

```bash
pip install -r requirements-dev.txt
```

## Конфигурация

Скопируйте `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

| Переменная          | Описание                                                |
|----------------------|-----------------------------------------------------------|
| `BOT_TOKEN`           | токен бота от @BotFather                                    |
| `ADMIN_IDS`           | список telegram id админов, формат `[123, 456]`             |
| `SUPPORT_CHAT_ID`     | id группы поддержки (с включёнными топиками)                |
| `SUPPORT_ORG_NAME`    | название организации для приветственного сообщения          |
| `DB__*`               | параметры подключения к БД (driver/host/port/user/...)       |

## Миграции БД

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Запуск

```bash
python -m app.main
```

## Лицензия

MIT — см. [LICENSE](LICENSE).
