import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def get_messages(conv_id: int, limit: int, connPool: asyncpg.Pool) -> DbResult:
    if (limit < -1 or conv_id <= -1):
        return DbResult(False, "wrong values for limit or conv_id")
    async with connPool.acquire() as conn:
        rows = await conn.fetch("SELECT user_id, content, id FROM messages WHERE conversation_id=$1 LIMIT $2",
            conv_id,
            limit
        )
    
    print(rows)
    
    return DbResult(True, rows, True)


@dbFunction
async def get_message(message_id: int, connPool: asyncpg.Pool) -> DbResult:
    if (message_id <= -1):
        return DbResult(False, "wrong value message_id")
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT user_id, content, conversation_id FROM messages WHERE id=$1", 
            message_id
        )
    
    return DbResult(True, row, True)



@dbFunction
async def add_message(conv_id: int, user_id: int, content: str, connPool: asyncpg.Pool) -> DbResult:
    if (user_id <= -1 or conv_id <= -1 or content==""):
        return DbResult(False, "wrong values for user_id or content or conv_id")
    async with connPool.acquire() as conn:
        message_id: int = await conn.fetchval(
            "INSERT INTO messages(conversation_id, user_id, content) VALUES($1,$2,$3) RETURNING id", 
            conv_id,
            user_id,
            content
        )
    
    return DbResult(True, {"result": message_id})