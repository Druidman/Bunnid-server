import json
from server.wsServer.objects.wsMessageType import WsMessageType


class WsMessage:
    def __init__(self, type: WsMessageType, status: bool, msg):
        self.type: WsMessageType = type
        self.status: bool = status
        self.msg = msg



    def getMsgStringified(self) -> str:
        return json.dumps(self.getMsg())

    def getMsg(self) -> dict:
        return {
            "TYPE": self.type,
            "STATUS": self.status,
            "MSG": self.msg
        }