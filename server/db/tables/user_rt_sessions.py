import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def check_if_token_in_db(token: str, connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if not token:
        return DbResult[None](error="No token provided") 
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM user_rt_sessions WHERE token=$1 LIMIT 1",token)
    if (row):
        return DbResult[bool](result=True)
    else:
        return DbResult[bool](result=False)
   
@dbFunction
async def add_token_to_db(token: str, connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if not token:
        return DbResult[None](error="No token provided") 
    
    async with connPool.acquire() as conn:
        await conn.execute("INSERT INTO user_rt_sessions(token) VALUES($1)",token)
    
    return DbResult[bool](result=True)


    
    