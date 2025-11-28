import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def get_messages(convId: int, limit: int, connPool: asyncpg.Pool) -> DbResult:
    if (limit < -1 or convId <= -1):
        return DbResult(False, "wrong values for limit and convId")
    async with connPool.acquire() as conn:
        rows = await conn.execute("SELECT userId, content FROM messages WHERE conversationId=:convId LIMIT :limit", {
            "convId": convId,
            "limit": limit
        })
    
    return DbResult(True, rows, True)


@dbFunction
async def get_message(messageId: int, connPool: asyncpg.Pool) -> DbResult:
    if (messageId <= -1):
        return DbResult(False, "wrong value messageId")
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT userId, content, conversationId FROM messages WHERE id=:messageId", {
            "messageId": messageId
        })
    
    return DbResult(True, row, True)



@dbFunction
async def add_message(convId: int, userId: int, content: str, connPool: asyncpg.Pool) -> DbResult:
    if (userId <= -1 or convId <= -1 or content==""):
        return DbResult(False, "wrong values for userId or content or convId")
    async with connPool.acquire() as conn:
        messageId = conn.fetchval(
            "INSERT INTO messages(conversationId, userId, content) VALUES($1,$2,$3) RETURNING id", 
            convId,
            userId,
            content
        )
    
    return DbResult(True, messageId)