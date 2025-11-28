
from fastapi import APIRouter, Body
from server.httpServer.auth.user_session import userSession
from server.db.tables.conversations import get_conversation, add_conversation, get_conversations
from server.db.tables.messages import get_messages, add_message
from server.db.tables.conversation_members import add_member, get_members
from server.eventPool.EventType import EventType
from server.eventPool.events.ConversationMsgEvent import ConversationMsgEventData

import server.globals as globals
from server.db.utils import DbResult

conversation_router = APIRouter(prefix="/conversation")




@conversation_router.get("/")
def conversationMain() -> str:
    return "<h1>This is conversation api!</h1>"


@conversation_router.post("/send")
@userSession
async def conversationSendMsg(
    conversationId: int = Body(...),
    msgContent: str = Body(...),
    userId: int = Body(...)
) -> globals.APIResponse:
    result: DbResult = await add_message(
        convId=conversationId, 
        userId=userId, 
        content=msgContent, 
        db=globals.connPool
    )
    print(f"FETCHED ID: {result.msg}")
    globals.eventPool.notify_event(EventType.NEW_MSG_IN_CONVERSATION, ConversationMsgEventData(conversationId, result.msg))
    return globals.api_response_from_db_repsonse(result)
  

@conversation_router.post("/getMessages")
@userSession
async def conversationGetMessages(conversationId: int = Body(...)) -> globals.APIResponse:
    result = await get_messages(convId=conversationId, limit=100, db=globals.connPool)

    return globals.api_response_from_db_repsonse(result)


@conversation_router.post("/create")
@userSession
async def conversationCreate(conversationTitle:str = Body(...)) -> globals.APIResponse:
    result = await add_conversation(title=conversationTitle, db=globals.connPool)

    return globals.api_response_from_db_repsonse(result)


@conversation_router.post("/addMember")
@userSession
async def conversationAddMember(
    conversationId: int = Body(...),
    memberId: int = Body(...)
) -> globals.APIResponse:
    result = await add_member(convId=conversationId, userId=memberId, db=globals.connPool)

    return globals.api_response_from_db_repsonse(result)

@conversation_router.post("/getMembers")
@userSession
async def conversationGetMembers(
    conversationId: int = Body(...)
) -> globals.APIResponse:
    result = await get_members(convId=conversationId, db=globals.connPool)

    return globals.api_response_from_db_repsonse(result)
    
@conversation_router.post("/get")
@userSession
async def conversationGet(
    conversationId: int = Body(...)
) -> globals.APIResponse:
    result = await get_conversation(convId=conversationId, db=globals.connPool)

    return globals.api_response_from_db_repsonse(result)


@conversation_router.post("/list")
@userSession
async def conversationList() -> globals.APIResponse:
    result: DbResult = await get_conversations(limit=100, db=globals.connPool)
    return globals.api_response_from_db_repsonse(result)


    

    
    




