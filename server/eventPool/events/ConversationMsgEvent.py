from server.eventPool.events.Event import Event
from server.eventPool.EventType import EventType
from server.eventPool.listeners.ConversationMsgEventListener import ConversationMsgEventListener

class ConversationMsgEvent(Event[ConversationMsgEventListener, int]):
    def __init__(self):
        super().__init__(EventType.NEW_MSG_IN_CONVERSATION)
        
    def notify_listeners(self, additionalEventInfo) -> None:
        if not additionalEventInfo:
            return # Because in this event this is required 
        
        print(f"ConversationMsgEvent notified with: {additionalEventInfo}")
        conversationId: int = additionalEventInfo

        for listener in self.listeners:
            if listener.conversationId == conversationId:
                print("Listener notified")
                listener()

        
    