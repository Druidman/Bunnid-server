import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def get_conversation(convId: int, connPool: asyncpg.Pool) -> DbResult:
    if (convId <= -1):
        return DbResult(False, "wrong convId")
    
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT title, id FROM conversations WHERE id=$1 LIMIT 1", 
            convId
        )

    if (not row):
        return DbResult(False, "No such conversation")
    return DbResult(True, row, True)

@dbFunction
async def get_conversations(limit: int, connPool: asyncpg.Pool) -> DbResult:
    if (limit <= 0):
        return DbResult(False, "wrong limit")
    async with connPool.acquire() as conn:
        rows = await conn.fetch("SELECT title, id FROM conversations LIMIT $1", 
            limit
        )
    
    if (not rows):
        return DbResult(False, "No conversations")
    
    return DbResult(True, rows, True)


@dbFunction
async def get_conversation_by_title(title: str, connPool: asyncpg.Pool) -> DbResult:
    if (title == ""):
        return DbResult(False, "wrong conv title")
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM conversations WHERE title=$1", 
            title
        )
    
    return DbResult(True, row, True)


@dbFunction
async def add_conversation(title: str, connPool: asyncpg.Pool) -> DbResult:
    if (title==""):
        return DbResult(False, "wrong title")
    async with connPool.acquire() as conn:
        conn.execute("INSERT INTO conversations(title) VALUES($1)", 
            title
        )
    
    return DbResult(True, True)