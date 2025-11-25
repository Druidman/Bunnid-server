from server.eventPool.events.Event import Event
from server.eventPool.EventType import EventType
from server.eventPool.listeners.ConversationMsgEventListener import ConversationMsgEventListener

class ConversationMsgEventData:
    def __init__(self, conversationId: int, messageId: int):
        self.conversationId = conversationId
        self.messageId = messageId

class ConversationMsgEvent(Event[ConversationMsgEventListener, ConversationMsgEventData]):
    def __init__(self):
        super().__init__(EventType.NEW_MSG_IN_CONVERSATION)
        
    def notify_listeners(self, additionalEventInfo) -> None:
        if not additionalEventInfo:
            return # Because in this event this is required 
        
        print(f"ConversationMsgEvent notified with: {additionalEventInfo.conversationId} {additionalEventInfo.messageId}")
        conversationId: int = additionalEventInfo.conversationId

        for listener in self.listeners:
            # print(str(listener.conversationId) + " " + str(conversationId))
            if listener.conversationId == conversationId:
                print("Listener notified")
                listener(additionalEventInfo.messageId)

        
    