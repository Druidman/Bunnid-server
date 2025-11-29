import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def get_conversation(conv_id: int, connPool: asyncpg.Pool) -> DbResult:
    if (conv_id <= -1):
        return DbResult[None](error="wrong conv_id")
    
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT title, id FROM conversations WHERE id=$1 LIMIT 1", 
            conv_id
        )

    if (not row):
        return DbResult[None](error="No such conversation")
    return DbResult[asyncpg.Record](result=row)

@dbFunction
async def get_conversations(limit: int, connPool: asyncpg.Pool) -> DbResult:
    if (limit <= 0):
        return DbResult[None](error="wrong limit")
    async with connPool.acquire() as conn:
        rows = await conn.fetch("SELECT title, id FROM conversations LIMIT $1", 
            limit
        )
    
    if (not rows):
        return DbResult[None](error="No conversations")
    
    return DbResult[list[asyncpg.Record]](result=rows)


@dbFunction
async def get_conversation_by_title(title: str, connPool: asyncpg.Pool) -> DbResult:
    if (title == ""):
        return DbResult[None](error="wrong conv title")
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM conversations WHERE title=$1", 
            title
        )
    
    return DbResult[asyncpg.Record](result=row)


@dbFunction
async def add_conversation(title: str, connPool: asyncpg.Pool) -> DbResult:
    if (title==""):
        return DbResult[None](error="wrong title")
    async with connPool.acquire() as conn:
        await conn.execute("INSERT INTO conversations(title) VALUES($1)", 
            title
        )
    
    return DbResult[bool](result=True)