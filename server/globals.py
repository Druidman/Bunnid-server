
import asyncpg, os
from server.db.utils import DbResult
from server.eventPool.EventPool import EventPool
from pydantic import BaseModel
from typing import Generic, Optional, TypeVar

T = TypeVar("T")
class APIResponse(BaseModel, Generic[T]):
    error: str
    response: Optional[T]

def validateObject(object: dict, keys: list[str]) -> bool:
    if type(object) != dict:
        return False
    return set(object.keys()) == set(keys)
 

def api_response_from_db_repsonse(result: DbResult, wrapperKey: str = "") -> APIResponse:
    if result.makeResultJsonable():
        if wrapperKey:
            return APIResponse(error=result.error, response={wrapperKey: result.resultJsonable})
        else:
            return APIResponse(error=result.error, response=result.resultJsonable)
    else:
        if wrapperKey:
            return APIResponse(error=result.error, response={wrapperKey: result.result})
        else:
            return APIResponse(error=result.error, response=result.result)
        


def API_RESPONSE(error: str ="", response: Optional[T] = None) -> APIResponse:
    return APIResponse(error=error, response=response)

def raise_exception(value: str):
    raise Exception(value)

RTS_TOKEN_LENGTH: int = 15
connPool: asyncpg.Pool | None = None
eventPool: EventPool = None

PRODUCTION = True if os.getenv("PRODUCTION") == "TRUE" else False
SESSION_TOKEN_EXPIRY_MINUTES = int(os.getenv("SESSION_TOKEN_EXPIRY_MINUTES", 10))
SESSION_TOKEN_SECRET_KEY = os.getenv("SESSION_TOKEN_SECRET_KEY", "")
SESSION_TOKEN_ALGORITHM = os.getenv("SESSION_TOKEN_ALGORITHM", "HS256")

SESSION_REFRESH_TOKEN_EXPIRY_HOURS = int(os.getenv("SESSION_REFRESH_TOKEN_EXPIRY_HOURS", 24))
SESSION_REFRESH_TOKEN_SECRET_KEY = os.getenv("SESSION_REFRESH_TOKEN_SECRET_KEY", "")
SESSION_REFRESH_TOKEN_ALGORITHM = os.getenv("SESSION_REFRESH_TOKEN_ALGORITHM", "HS256")



errors = {

    "NO_JSON": API_RESPONSE(error="No json found in request"),
    "ACCES_DENIED": API_RESPONSE(error="Acces denied"),
    "NO_ARGS": API_RESPONSE(error="No args found in request"),
    "INCORRECT_LOGIN_VALUES": API_RESPONSE(error="Incorrect login or password"),
    "LOGIN_TRY_AGAIN": API_RESPONSE(error="Smth went wrong try loggin in again"),
    "FAILED_TO_ASSIGN_TOKEN": API_RESPONSE(error="Failed to assign token to the user")
}


