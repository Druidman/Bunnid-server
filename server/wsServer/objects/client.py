
import websockets.sync.server as websockets
from server.wsServer.communication.wsMessage import WsMessage
from server.wsServer.communication.wsMessageType import WsMessageType
from typing import List
import time, json

from server.db.tables.userRTSessions import check_if_token_in_db
import server.globals as globals
from server.db.utils import DbResult

from server.eventPool.listeners.ConversationMsgEventListener import ConversationMsgEventListener
from server.eventPool.listeners.EventListener import EventListener
 
class Client:
    def __init__(self, connection: websockets.ServerConnection):
        self.connection = connection

        self.messages: List[WsMessage] = []

        self.end = False

        self.msgReceiverOn = False
        self.eventSenders: List[EventListener] = []

    def authenticate(self) -> bool:
        requestToken: WsMessage = WsMessage(WsMessageType.TOKEN__REQ, True, "")
        accessGranted: WsMessage = WsMessage(WsMessageType.ACCESS_GRANTED__INFO, True, "")
        accessDenied: WsMessage = WsMessage(WsMessageType.ACCESS_DENIED__INFO, True, "")


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
        
        if msg["TYPE"] != WsMessageType.TOKEN__RES:
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
    
    def sendNewConversationMsg(self, conversationId: int) -> None: 
        # TODO
        print(f"sending new conversation msg TODO ID: {conversationId}")
        



    def registerNewConversationMsgEventListener(self, conversationId: int) -> None:
        listener: ConversationMsgEventListener = ConversationMsgEventListener(self.sendNewConversationMsg, conversationId=conversationId)
        globals.conversation_msg_event.add_listener(listener)
        self.eventSenders.append(listener)

    def handleRtMessagesInConversationRequest(self, msg: WsMessage) -> None:
        print("Rt messaging req")
        if not msg.msg:
            self.sendMsg(WsMessage(WsMessageType.RT_MESSAGES_IN_CONVERSATION__RES, True, False))
            print("Rt messaging req denied")
        else:
            self.registerNewConversationMsgEventListener(msg.msg)
            self.sendMsg(WsMessage(WsMessageType.RT_MESSAGES_IN_CONVERSATION__RES, True, True))
            print("Rt messaging req granted")
        
    def handleRequestMessage(self,msg: WsMessage) -> None:
        if msg.type == WsMessageType.RT_MESSAGES_IN_CONVERSATION__REQ:
            self.handleRtMessagesInConversationRequest(msg)
            
        else:
            pass


    def msgReceiver(self):
        self.msgReceiverOn = True

        while not self.end:
            try:
                msg = self.connection.recv()
                msg: dict = json.loads(msg)
                if not msg:
                    continue

                print(f"NEW MSG THRU WS: {msg}")

                msg_type = msg.get("TYPE")
                msg_status = msg.get("STATUS")
                msg_msg = msg.get("MSG")

                if not msg_type or not msg_status or not msg_msg:
                    continue

                msg = WsMessage(msg_type, msg_status, msg_msg)
                if msg.type in WsMessageType.requests:
                    self.handleRequestMessage(msg)
                else:
                    self.messages.append(msg)
            except:
                break

        self.msgReceiverOn = False
