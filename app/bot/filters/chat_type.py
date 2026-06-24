from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: str | tuple[str, ...]) -> None:
        self.chat_type = chat_type

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        chat = event.chat if isinstance(event, Message) else event.message.chat
        if isinstance(self.chat_type, str):
            return chat.type == self.chat_type
        return chat.type in self.chat_type
