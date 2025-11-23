from .EventListener import EventListener
from typing import Callable

class ConversationMsgEventListener(EventListener[Callable[[int],None]]):
    def __init__(self, callback: Callable[[int],None], conversationId: int):
        self.conversationId = conversationId
        super().__init__(callback)
        
    def __call__(self) -> None:
        
        return self.listener_callback(self.conversationId)