from server.db.tables.user_rt_sessions import check_if_token_in_db
from server.db.utils import DbResult
from fastapi import Header, HTTPException
import server.globals as globals

async def check_if_valid_rts_token(token: str) -> bool:
    if (token == ""): return False
    if (len(token) < globals.RTS_TOKEN_LENGTH): return False

    result: DbResult = await check_if_token_in_db(token, globals.connPool) 
    if not result.status:
        return False
    return result.msg

async def verify_rts(token: str = Header(..., alias="X-RTS-Token")):
    if (not await check_if_valid_rts_token(token)):
        raise HTTPException(status_code=401, detail="Wrong RTS token")
    