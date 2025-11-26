import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def get_members(convId: int, connPool: asyncpg.Pool) -> DbResult:
    if (convId <= -1):
        return DbResult(False, "wrong convId")
    
    async with connPool.acquire() as conn:
        rows = await conn.fetch("SELECT userId FROM conversation_members WHERE conversationId=:convId", {
            "convId": convId
        })

    return DbResult(True, rows, True)


@dbFunction
async def add_member(convId: int,userId: int, connPool: asyncpg.Pool) -> DbResult:
    if (convId <= -1 or userId <= -1):
        return DbResult(False, "wrong convId or userId")
    
    async with connPool.acquire() as conn:
        conn.execute("INSERT INTO conversation_members(conversationId, userId) VALUES(:convId, :userId)", {
            "convId": convId,
            "userId": userId,
        })
    return DbResult(True, True)