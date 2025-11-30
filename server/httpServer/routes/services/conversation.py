
from ast import Dict
from typing import TypedDict
from fastapi import APIRouter, Body
from server.db.tables.conversations import get_conversation, add_conversation, get_conversations
from server.db.tables.messages import get_messages, add_message
from server.db.tables.conversation_members import add_member, get_members
from server.eventPool.EventType import EventType
from server.eventPool.events.ConversationMsgEvent import ConversationMsgEventData

import server.globals as globals
from server.db.utils import DbResult
from pydantic import BaseModel

conversation_router = APIRouter(prefix="/conversation")




@conversation_router.get("/")
def conversationMain() -> str:
    return "<h1>This is conversation api!</h1>"

class ConversationSendResponse(BaseModel):
    message_id: int

@conversation_router.post("/send")
async def conversationSendMsg(
    conversationId: int = Body(...),
    msgContent: str = Body(...),
    userId: int = Body(...)
) -> globals.APIResponse[ConversationSendResponse]:
    result: DbResult = await add_message(
        conv_id=conversationId, 
        user_id=userId, 
        content=msgContent, 
        connPool=globals.connPool
    )
    print(f"FETCHED ID: {result.result}")
    await globals.eventPool.notify_event(EventType.NEW_MSG_IN_CONVERSATION, ConversationMsgEventData(conversationId, result.msg))
    return globals.api_response_from_db_repsonse(result,wrapperKey="message_id")
  


class MessageElement(TypedDict):
    user_id: int
    content: str
    id: int
class ConversationGetMessagesResponse(BaseModel):
    messages: list[MessageElement]

@conversation_router.post("/getMessages")
async def conversationGetMessages(conversationId: int = Body(embed=True)) -> globals.APIResponse[ConversationGetMessagesResponse]:
    result = await get_messages(conv_id=conversationId, limit=100, connPool=globals.connPool)

    return globals.api_response_from_db_repsonse(result,wrapperKey="messages")



class ConversationCreateResponse(BaseModel):
    result: bool

@conversation_router.post("/create")
async def conversationCreate(conversationTitle:str = Body(embed=True)) -> globals.APIResponse[ConversationCreateResponse]:
    result = await add_conversation(title=conversationTitle, connPool=globals.connPool)

    return globals.api_response_from_db_repsonse(result, wrapperKey="result")


class ConversationAddMemberResponse(BaseModel):
    result: bool

@conversation_router.post("/addMember")
async def conversationAddMember(
    conversationId: int = Body(...),
    memberId: int = Body(...)
) -> globals.APIResponse[ConversationAddMemberResponse]:
    result = await add_member(conv_id=conversationId, user_id=memberId, connPool=globals.connPool)

    return globals.api_response_from_db_repsonse(result, wrapperKey="result")


class ConversationMember(TypedDict):
    user_id: int
class ConversationGetMembersResponse(BaseModel):
    members: list[ConversationMember]
@conversation_router.post("/getMembers")
async def conversationGetMembers(
    conversationId: int = Body(embed=True)
) -> globals.APIResponse[ConversationGetMembersResponse]:
    result = await get_members(conv_id=conversationId, connPool=globals.connPool)

    return globals.api_response_from_db_repsonse(result)

class ConversationModel(BaseModel):
    title: str
    id: int
class ConversationGetResponse(BaseModel):
    conversation: ConversationModel
@conversation_router.post("/get")
async def conversationGet(
    conversationId: int = Body(embed=True)
) -> globals.APIResponse[ConversationGetResponse]:
    result = await get_conversation(conv_id=conversationId, connPool=globals.connPool)

    return globals.api_response_from_db_repsonse(result)

class ConversationListResponse(BaseModel):
    conversations: list[ConversationModel]

@conversation_router.get("/list")
async def conversationList() -> globals.APIResponse[ConversationListResponse]:
    result: DbResult = await get_conversations(limit=100, connPool=globals.connPool)
    return globals.api_response_from_db_repsonse(result)


    

    
    




