from .EventType import EventType
from .EventPool import EventPool
from .events.Event import Event
import server.globals as globals

__all__ = ["EventType","EventPool","Event"]




def setupEventPool() -> None:
    globals.eventPool = EventPool()