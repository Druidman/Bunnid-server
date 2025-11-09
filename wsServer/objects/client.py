
import websockets.sync.server as websockets
from server.wsServer.objects.wsMessage import WsMessage
from server.wsServer.objects.wsMessageType import WsMessageType
from typing import List
import time, json

from server.db.tables.userRTSessions import check_if_token_in_db
import server.globals as globals
from server.db.utils import DbResult
 
class Client:
    def __init__(self, connection: websockets.ServerConnection):
        self.connection = connection

        self.messages: List[dict] = []

        self.end = False

        self.msgReceiverOn = False

    def authenticate(self) -> bool:
        requestToken: WsMessage = WsMessage(WsMessageType.REQUEST_TOKEN_MSG_TYPE, True, "")
        accessGranted: WsMessage = WsMessage(WsMessageType.ACCESS_GRANTED_MSG_INFO_TYPE, True, "")
        accessDenied: WsMessage = WsMessage(WsMessageType.ACCESS_DENIED_MSG_INFO_TYPE, True, "")


        if not self.sendMsg(requestToken): 
            return False
        print("sent token request")
        
        msg = None
        try:
            msg = self.connection.recv(timeout=10)
            msg = json.loads(msg)
                
        except:
            self.sendMsg(accessDenied)
            return False
        
        
        if not msg:
            self.sendMsg(accessDenied)
            return False
        
        print("got response with msg ")
        
        if msg["TYPE"] != WsMessageType.RETURN_TOKEN_MSG_TYPE:
            self.sendMsg(accessDenied)
            return False
        
        token = msg["MSG"]
        
        dbRes: DbResult = check_if_token_in_db(token, globals.dbConn.cursor())
        if not dbRes.status:
            self.sendMsg(accessDenied)
            return False
        
        return self.sendMsg(accessGranted)
        

    def getMsg(self, block: bool = False, timeout = None) -> dict | None:
        if (len(self.messages)):
            self.messages[0]
        
        if timeout:
            startTime = time.time()
            
            while not len(self.messages) and (startTime + timeout < time.time()): pass

            if (len(self.messages)):
                return self.messages[0]
            
            return None

        if block:
            while not len(self.messages): pass

            return self.messages[0]
        return None
    
    def sendMsg(self, msg: WsMessage) -> bool:
        try:
            self.connection.send(msg.getMsgStringified())
            return True
        except:
            return False
        



    def msgReceiver(self):
        self.msgReceiverOn = True

        while not self.end:
            try:
                msg = self.connection.recv()
                msg = json.loads(msg)
                self.messages.append(msg)
            except:
                break

        self.msgReceiverOn = False
