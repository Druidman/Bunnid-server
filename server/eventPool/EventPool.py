from server.server.eventPool import ConversationMsgEvent
from .EventType import EventType
from .events.Event import Event
from typing import Dict


class EventPool:
    def __init__(self):
        self.events: Dict[EventType, Event ] = {
            EventType.NEW_MSG_IN_CONVERSATION: ConversationMsgEvent(),
            EventType.NEW_CONVERSATION: None
        }

    async def notify_event(self, eventType: EventType, additionalEventInfo=None) -> bool:
        if not self.checkIfValidEventType(eventType):
            return False
        
        await self.events[eventType].notify(additionalEventInfo)


        return True
    
    def checkIfValidEventType(self, event_type: EventType) -> bool:
        if event_type not in self.events.keys():
            return False
        else:
            return True

    
        