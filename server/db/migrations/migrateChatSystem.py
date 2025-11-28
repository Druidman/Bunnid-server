import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_chat_system(connPool: asyncpg.Pool) -> DbResult:
    
    async with connPool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS messages(" \
                "id SERIAL PRIMARY KEY," \
                "conversationId INTEGER," \
                "userId INTEGER," \
                "content TEXT" \
            ")"
        )
        

        await conn.execute("CREATE TABLE IF NOT EXISTS conversations(" \
                "id SERIAL PRIMARY KEY," \
                "title TEXT" \
            ")"
        )
        

        await conn.execute("CREATE TABLE IF NOT EXISTS conversation_members(" \
                "conversationId SERIAL PRIMARY KEY," \
                "userId INTEGER" \
            ")"
        )
    
    return DbResult(True, True)
    
    