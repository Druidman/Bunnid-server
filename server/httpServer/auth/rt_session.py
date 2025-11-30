import secrets
from server.db.tables.user_rt_sessions import check_if_token_in_db, add_token_to_db
from server.db.utils import DbResult
from fastapi import Header, HTTPException
import server.globals as globals


async def make_RTS() -> str:

    RTS_token = secrets.token_urlsafe(globals.RTS_TOKEN_LENGTH)
    result: DbResult[bool | None] = await add_token_to_db(token=RTS_token, connPool=globals.connPool)
    if result.error:
        print(f"Error when adding RT token: {result.error}")
        return ""
    else:
        return RTS_token

async def check_if_valid_rts_token(token: str) -> bool:
    if (token == ""): return False
    if (len(token) < globals.RTS_TOKEN_LENGTH): return False

    result: DbResult[bool | None] = await check_if_token_in_db(token, globals.connPool) 
    if result.error:
        return False
    return result.result

async def verify_rts(token: str = Header(..., alias="X-RTS-Token")):
    if (not await check_if_valid_rts_token(token)):
        raise HTTPException(status_code=401, detail="Wrong RTS token")
    