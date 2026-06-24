from aiogram import Router

from app.bot.handlers import group, language, start, support


def get_handlers_router() -> Router:
    router = Router(name="handlers")
    router.include_routers(start.router, language.router, support.router, group.router)
    return router
