from .EventType import EventType
from .events.Event import Event
from typing import Dict, List


class EventPool:
    def __init__(self):
        self.events: Dict[EventType, List[ Event ] ] = {}

    async def notify_event(self, eventType: EventType, additionalEventInfo=None) -> bool:
        if not self.checkIfValidEventType(eventType):
            return False
        
        for event in self.events[eventType]:
            await event.notify(additionalEventInfo)


        return True
    
    def addEventType(self, event_type: EventType) -> bool:
        if self.checkIfValidEventType(event_type):
            return False
        
        self.events[event_type] = []
        return True
    
    def removeEventType(self, event_type: EventType) -> bool:
        if not self.checkIfValidEventType(event_type):
            return False
        
        self.events.pop(event_type)
        return True
    
    def clearAllEvents(self) -> bool:
        self.events = {}
        return True
    
    def removeEvents(self, eventType: EventType) -> bool:
        if not self.checkIfValidEventType(eventType):
            return False
        
        self.events[eventType] = []
        return True

    def checkIfValidEventType(self, event_type: EventType) -> bool:
        if event_type not in self.events.keys():
            return False
        else:
            return True

    def registerEvent(self,event: Event) -> bool:
        if not self.checkIfValidEventType(event.event_type):
            return False
        
        self.events[event.event_type].append(event)
        return True

    def removeEvent(self,event: Event) -> bool:
        if not self.checkIfValidEventType(event.event_type):
            return False
        
        self.events[event.event_type].remove(event)
        return True
        