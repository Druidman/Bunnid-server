import json
from .wsEvent import WsEvent


class WsMessage:
    def __init__(self, event: WsEvent, error: str, requestId: int, data: dict):
        self.event: WsEvent = event
        self.error: str = error
        self.requestId: int = requestId
        self.data: dict = data



    def getMsgStringified(self) -> str:
        return json.dumps(self.getMsg())

    def getMsg(self) -> dict:
        return {
            "data": self.data,
            "error": self.error,
            "requestId": self.requestId,
            "event": self.event
        }