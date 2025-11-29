
import asyncpg
from server.db.utils import DbResult
from server.eventPool.EventPool import EventPool
from server.eventPool.events.ConversationMsgEvent import ConversationMsgEvent
from pydantic import BaseModel


class APIResponse(BaseModel):
    STATUS: bool
    MSG: dict | str | bool | list

def validateObject(object: dict, keys: list[str]) -> bool:
    return set(object.keys()) == set(keys)
 

def api_response_from_db_repsonse(result: DbResult) -> APIResponse:
    print(f"DICT: {result.msgObject}")
    print(f"MSG: {result.msg}")
    if result.makeMsgObject():
        return APIResponse(STATUS=result.status, MSG=result.msgObject)
    else:
        return APIResponse(STATUS=result.status, MSG=result.msg)

def API_RESPONSE(stat: bool, msg: dict | str | bool) -> APIResponse:
    return APIResponse(STATUS=stat, MSG=msg)


USER_TOKEN_LENGTH: int = 15
RTS_TOKEN_LENGTH: int = 15
connPool: asyncpg.Pool | None = None
eventPool: EventPool = None
conversation_msg_event: ConversationMsgEvent = None


errors = {

    "NO_JSON": API_RESPONSE(False, "No json found in request"),
    "ACCES_DENIED": API_RESPONSE(False, "Acces denied"),
    "NO_ARGS": API_RESPONSE(False, "No args found in request"),
    "INCORRECT_LOGIN_VALUES": API_RESPONSE(False, "Incorrect login or password"),
    "LOGIN_TRY_AGAIN": API_RESPONSE(False, "Smth went wrong try loggin in again"),
    "FAILED_TO_ASSIGN_TOKEN": API_RESPONSE(False, "Failed to assign token to the user")
}


