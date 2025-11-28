
import secrets
from fastapi import Header, HTTPException

from server import globals
from server.db.tables.userSessions import check_if_token_in_db, add_token_to_db
from server.db.utils import DbResult

async def check_if_valid_token(token: str) -> bool:
    if (token == ""): return False
    if (len(token) < globals.USER_TOKEN_LENGTH): return False

    result: DbResult = await check_if_token_in_db(token, globals.dbConn)  # TODO: verify if globals.dbConn is asyncpg.Pool
    if not result.status:
        return False
    return result.msg

async def make_user_session(userId: str) -> str:
    token: str = secrets.token_urlsafe(globals.USER_TOKEN_LENGTH)
    result: DbResult = await add_token_to_db(token=token, userId=userId, connPool=globals.dbConn)  # TODO: verify if globals.dbConn is asyncpg.Pool
    if not result.status:
        print(f"Error when adding token: {result.msg}")
        return ""
    else:
        return token


async def verify_user_session(token: str = Header(..., alias="X-User-Session-Token")):
    if (not await check_if_valid_token(token)):
        raise HTTPException(status_code=401, detail="Wrong user session token")
    
    