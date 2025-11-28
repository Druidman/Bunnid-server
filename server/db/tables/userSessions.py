import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def check_if_token_in_db(token: str, connPool: asyncpg.Pool) -> DbResult:
    if not token:
        return DbResult(True, False) 
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM UserSessions WHERE token=:token LIMIT 1",{"token": token})
    if (row):
        return DbResult(True, True)
    else:
        return DbResult(True, False) 
   
@dbFunction
async def add_token_to_db(token: str, userId: int,  connPool: asyncpg.Pool) -> DbResult:
    if (userId <= -1 or not token):
        return DbResult(False, "Wrong token or userId")
    async with connPool.acquire() as conn:
        await conn.execute("INSERT INTO UserSessions(token, userId) VALUES(:token, :userId)",{"token": token, "userId": userId})
    
    return DbResult(True, True)


@dbFunction
async def get_token_data(token: str, connPool: asyncpg.Pool) -> DbResult:
    if ( not token):
        return DbResult(False, "Wrong token")
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT userId, id FROM UserSessions WHERE token=:token LIMIT 1",{"token": token})
    
    
    if not row:
        return DbResult(False, "")
    return DbResult(True, row, True)


    
    