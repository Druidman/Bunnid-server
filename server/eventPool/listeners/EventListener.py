from typing import  TypeVar, Generic
from abc import ABC, abstractmethod


T = TypeVar('T')

class EventListener(Generic[T], ABC):
    
    def __init__(self, callback: T):
        self.listener_callback: T = callback

    @abstractmethod
    async def __call__(self) -> None: pass
