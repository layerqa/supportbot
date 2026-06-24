from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.filters.chat_type import ChatTypeFilter

router = Router(name="start")
router.message.filter(ChatTypeFilter("private"))


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Опишите вашу проблему одним сообщением, "
        "и мы передадим её в поддержку."
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Просто напишите сообщение — мы создадим тикет и ответим здесь."
    )
