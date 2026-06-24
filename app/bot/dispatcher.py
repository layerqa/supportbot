from aiogram import Dispatcher

from app.bot.handlers import get_handlers_router
from app.bot.middlewares.db import DbSessionMiddleware
from app.db.session import async_session_factory


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.update.middleware(DbSessionMiddleware(async_session_factory))
    dispatcher.include_router(get_handlers_router())
    return dispatcher
