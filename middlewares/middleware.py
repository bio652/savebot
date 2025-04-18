from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, TelegramObject

import config

class SpamMiddleware(BaseMiddleware):
    def __init__(self, mininterv: float = 2):
        super().__init__()
        self.mininterv = mininterv
        self.lastMessageTime = {}
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.from_user is not None:
            if "https://" not in event.text and "/" not in event.text:
                return 
            curtime = event.date
            lasttime = self.lastMessageTime.get(event.from_user.id)
            if lasttime is not None:
                interval = (curtime - lasttime).total_seconds()
                if interval < self.mininterv:
                    return
            self.lastMessageTime[event.from_user.id] = curtime
        result = await handler(event, data)
        return result
    
class AdminCheckerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if str(event.from_user.id) in config.ADMINS:
            return await handler(event, data)
        return