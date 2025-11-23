from typing import  List, Generic, TypeVar
from ..EventType import EventType
from ..listeners.EventListener import EventListener
from abc import abstractmethod, ABC

T = TypeVar('T')
B = TypeVar('B')

class Event(ABC, Generic[T, B]):
    
    def __init__(self, event_type: EventType):
        self.listeners: List[ T ] = []
        self.event_type: EventType = event_type


    def add_listener(self,listener: T) -> bool:
        if not listener:
            return False
        
        self.listeners.append(listener)
        return True

    def remove_listener(self,listener: T) -> bool:
        if not listener:
            return True #like not existent so removed XD
        
        self.listeners.remove(listener)
        return True


    def notify(self, additionalEventInfo: B = None) -> None:
        return self.notify_listeners(additionalEventInfo)
    
    @abstractmethod
    def notify_listeners(self, additionalEventInfo: B = None): pass
