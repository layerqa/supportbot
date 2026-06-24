from aiogram import Router

from app.bot.handlers import group, start, support


def get_handlers_router() -> Router:
    router = Router(name="handlers")
    router.include_routers(start.router, support.router, group.router)
    return router
