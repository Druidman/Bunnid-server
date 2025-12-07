import asyncpg
from ..utils import DbResult, dbFunction
import datetime

@dbFunction
async def check_if_token_in_db(id: int, connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if not id:
        return DbResult[None](error="No token_id provided") 
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT 1 FROM session_refresh_tokens WHERE id=$1",id)
    if (row):
        return DbResult[bool](result=True) 
    else:
        return DbResult[bool](result=False) 
   
@dbFunction
async def add_token_to_db(user_id: int, created_at: datetime.date, expires_at: datetime.date, connPool: asyncpg.Pool) -> DbResult[None | int]:
    if (user_id <= -1 or not created_at or not expires_at):
        return DbResult[None](error="Wrong user_id or datetime for creation and expiration")
    async with connPool.acquire() as conn:
        result: int = await conn.fetchval(
            "INSERT INTO session_refresh_tokens(user_id, created_at, expires_at) VALUES($1,$2,$3) RETURNING id", 
            user_id, 
            created_at,
            expires_at
        )
    if result:
        return DbResult[int](result=result) 

    return DbResult[None](error="No token id returned by db") 



@dbFunction
async def check_if_token_revoked(id: int, connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if not id:
        return DbResult[None](error="No token_id provided") 
    

    async with connPool.acquire() as conn:
        row: asyncpg.Record = await conn.fetchrow("SELECT revoked FROM session_refresh_tokens WHERE id=$1",id)

    if not row:
        return DbResult[bool](result=False) 
    
    
    if row.get("revoked"):
        return DbResult[bool](result=True)
    else:
        return  DbResult[bool](result=False)

        
   

    
    