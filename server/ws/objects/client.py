

from server.ws.communication.wsMessage import WsMessage
from server.ws.communication.wsEvent import WsEvent
from typing import Callable, List


from server.db.tables.messages import get_message
import server.globals as globals
from server.db.utils import DbResult
from itertools import count

from server.eventPool.listeners.ConversationMsgEventListener import ConversationMsgEventListener
from server.eventPool.listeners.EventListener import EventListener
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
 
class Client:
    def __init__(self, connection: WebSocket):
        self.connection = connection

        self.eventSenders: List[EventListener] = []

        self.msgResponseWaiters: dict[int, Callable[[WsMessage], None]] = {}
        self.eventHandlers: dict[WsEvent, Callable[[WsMessage], None]] = {
            WsEvent.RT_MESSAGES_IN_CONVERSATION: self.handleRtMessagesInConversationMsg
        }
        self.requestIdGen = count(1,1)
    
    async def sendMsg(self, msg: WsMessage) -> bool:
        try:
            await self.connection.send_json(msg.getMsg(), mode = "text")
            return True
        except:
            return False
    
    async def sendNewConversationMsg(self,messageId: int) -> None: 
        print(f"sending new conversation msg TODO ID: {messageId}")
        messageRes: DbResult = await get_message(messageId, globals.connPool)
        if messageRes.error:
            return
        
        if messageRes.makeResultJsonable():
            await self.sendMsg(WsMessage(WsEvent.NEW_CONVERSATION_MSG__INFO, "", next(self.requestIdGen), messageRes.resultJsonable))
        
    def registerNewConversationMsgEventListener(self, conversationId: int) -> None:
        listener: ConversationMsgEventListener = ConversationMsgEventListener(self.sendNewConversationMsg, conversationId=int(conversationId))
        globals.conversation_msg_event.add_listener(listener)
        self.eventSenders.append(listener)

    async def handleRtMessagesInConversationMsg(self, msg: WsMessage) -> None:
        if not globals.validateObject(msg.data, keys=["conversationId"]) or msg.event != WsEvent.RT_MESSAGES_IN_CONVERSATION or msg.error:
            await self.sendMsg(WsMessage(
                WsEvent.RT_MESSAGES_IN_CONVERSATION,
                "",
                msg.requestId,
                {
                    "result": False
                }
            ))
            print("Rt messaging req denied")
        else:
            self.registerNewConversationMsgEventListener(msg.data.get("conversationId"))
            await self.sendMsg(WsMessage(
                WsEvent.RT_MESSAGES_IN_CONVERSATION,
                "",
                msg.requestId,
                {
                    "result": True
                }
            ))
            print("Rt messaging req granted")
        

    def getEventHandler(self, event: WsEvent) -> Callable[[WsMessage], None] | None:
        return self.eventHandlers.get(event)

    async def handleMsg(self, msg: WsMessage):
        if msg.requestId in self.msgResponseWaiters:
            waiter = self.msgResponseWaiters.get(msg.requestId)
            await waiter(msg)
        else:
            
            eventHandler = self.getEventHandler(msg.event)

            if eventHandler: 
                await eventHandler(msg)
            else:
                await self.sendMsg(WsMessage(WsEvent.INVALID_EVENT, "", msg.requestId, {}))

    async def receiveMsg(self):
        
        try:
            msg = await self.connection.receive_json()
        
            print(f"NEW MSG THRU WS: {type(msg)}")

            if not globals.validateObject(msg, ["event", "data", "requestId", "error"]):
                return
            
            print(f"Handling msg: {msg}")

            msg = WsMessage(msg["event"], msg["error"], msg["requestId"], msg["data"])
    
            await self.handleMsg(msg)


            
        except WebSocketDisconnect:
            raise
        except WebSocketException:
            raise
        except Exception as e:
            print(f"Exception in msgReceviver: {e}")
      
