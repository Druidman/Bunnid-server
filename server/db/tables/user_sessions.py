import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def check_if_token_in_db(token: str, connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if not token:
        return DbResult[None](error="No token provided") 
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM user_sessions WHERE token=$1 LIMIT 1",token)
    if (row):
        return DbResult[bool](result=True) 
    else:
        return DbResult[bool](result=False) 
   
@dbFunction
async def add_token_to_db(token: str, user_id: int,  connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if (user_id <= -1 or not token):
        return DbResult[None](error="Wrong token or user_id")
    async with connPool.acquire() as conn:
        await conn.execute("INSERT INTO user_sessions(token, user_id) VALUES($1,$2)",token, user_id)
    
    return DbResult[bool](result=True) 


@dbFunction
async def get_token_data(token: str, connPool: asyncpg.Pool) -> DbResult[None | asyncpg.Record]:
    if ( not token):
        return DbResult[None](error="Wrong token")
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT user_id, id FROM user_sessions WHERE token=$1 LIMIT 1",token)
    
    
    if not row:
        return DbResult[None](error="Token not found")
    return DbResult[asyncpg.Record](result=row)


    
    