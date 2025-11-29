from enum import Enum

class WsEvent(str, Enum):
    RT_MESSAGES_IN_CONVERSATION = "RT_MESSAGES_IN_CONVERSATION"
    NEW_CONVERSATION_MSG__INFO = "NEW_CONVERSATION_MSG__INFO" # info means does not expect return
    INVALID_EVENT = "INVALID_EVENT"
    
