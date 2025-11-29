import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def get_members(conv_id: int, connPool: asyncpg.Pool) -> DbResult[None | list[asyncpg.Record]]:
    if (conv_id <= -1):
        return DbResult[None](error="wrong conv_id")
    
    async with connPool.acquire() as conn:
        rows = await conn.fetch("SELECT user_id FROM conversation_members WHERE conversation_id=$1", 
            conv_id
        )

    return DbResult[list[asyncpg.Record]](result=rows)


@dbFunction
async def add_member(conv_id: int,user_id: int, connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if (conv_id <= -1 or user_id <= -1):
        return DbResult[None](error="wrong conv_id or user_id")
    
    async with connPool.acquire() as conn:
        conn.execute("INSERT INTO conversation_members(conversation_id, user_id) VALUES($1,$2)", 
            conv_id,
            user_id,
        )
    return DbResult[bool](result=True)