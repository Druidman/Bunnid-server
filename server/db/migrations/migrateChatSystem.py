import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_chat_system(connPool: asyncpg.Pool) -> DbResult:
    
    async with connPool.acquire() as conn:
        await conn.execute("""CREATE TABLE IF NOT EXISTS messages(
                id SERIAL PRIMARY KEY,
                conversation_id INTEGER,
                user_id INTEGER,
                content TEXT
            )"""
        )
        

        await conn.execute("""CREATE TABLE IF NOT EXISTS conversations(
                id SERIAL PRIMARY KEY,
                title TEXT
            )"""
        )
        

        await conn.execute("""CREATE TABLE IF NOT EXISTS conversation_members(
                conversation_id INTEGER,
                user_id INTEGER
            )"""
        )
    
    return DbResult(True, True)
    
    