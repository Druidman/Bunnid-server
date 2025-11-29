from .EventListener import EventListener
from typing import Callable
import asyncio

class ConversationMsgEventListener(EventListener[Callable[[int],None]]):
    def __init__(self, callback: Callable[[int],None], conversationId: int):
        self.conversationId = conversationId
        super().__init__(callback)
        
    async def __call__(self, messageId: int) -> None:
        if asyncio.iscoroutinefunction(self.listener_callback):
        
            return await self.listener_callback(messageId)
        else:
            self.listener_callback(messageId)