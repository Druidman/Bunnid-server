from .EventType import EventType
from .EventPool import EventPool
from .events.Event import Event
from .events.ConversationMsgEvent import ConversationMsgEvent
import server.globals as globals

__all__ = ["EventType","EventPool","Event"]




def setupEventPool() -> None:
    event_pool: EventPool = EventPool()


    conversation_msg_event = ConversationMsgEvent()

    event_pool.addEventType(EventType.NEW_MSG_IN_CONVERSATION)
    event_pool.registerEvent(conversation_msg_event)

    globals.eventPool = event_pool
    globals.conversation_msg_event = conversation_msg_event