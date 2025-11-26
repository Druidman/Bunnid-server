import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def check_if_token_in_db(token: str, connPool: asyncpg.Pool) -> DbResult:
    if not token:
        return DbResult(True, False) 
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM UserRTSessions WHERE token=:token LIMIT 1",{"token": token})
    if (row):
        return DbResult(True, True)
    else:
        return DbResult(True, False) 
   
@dbFunction
async def add_token_to_db(token: str, connPool: asyncpg.Pool) -> DbResult:
    if not token:
        return DbResult(True, False) 
    
    async with connPool.acquire() as conn:
        conn.execute("INSERT INTO UserRTSessions(token) VALUES(:token)",{"token": token})
    
    return DbResult(True, True)


    
    