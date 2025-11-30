
import secrets
from fastapi import Header, HTTPException

import server.globals as globals
from server.db.tables.user_sessions import check_if_token_in_db, add_token_to_db

from server.db.utils import DbResult

async def check_if_valid_token(token: str) -> bool:
    if (token == ""): return False
    if (len(token) < globals.USER_TOKEN_LENGTH): return False

    result: DbResult[bool | None] = await check_if_token_in_db(token, globals.connPool) 
    if result.error:
        return False
    return result.result



async def make_user_session(user_id: str) -> str:
    token: str = secrets.token_urlsafe(globals.USER_TOKEN_LENGTH)
    result: DbResult = await add_token_to_db(token=token, user_id=user_id, connPool=globals.connPool)  
    if result.error:
        print(f"Error when adding token: {result.error}")
        return ""
    else:
        return token


async def verify_user_session(token: str = Header(..., alias="X-User-Session-Token")):
    if (not await check_if_valid_token(token)):
        raise HTTPException(status_code=401, detail="Wrong user session token")
    


    