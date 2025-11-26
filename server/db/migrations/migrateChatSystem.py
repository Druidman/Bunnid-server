import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_chat_system(connPool: asyncpg.Pool) -> DbResult:
    
    async with connPool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS messages(" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "conversationId INTEGER," \
                "userId INTEGER," \
                "content TEXT" \
            ")"
        )
        

        await conn.execute("CREATE TABLE IF NOT EXISTS conversations(" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "title TEXT" \
            ")"
        )
        

        await conn.execute("CREATE TABLE IF NOT EXISTS conversation_members(" \
                "conversationId INTEGER PRIMARY KEY AUTOINCREMENT," \
                "userId INTEGER" \
            ")"
        )
    
    return DbResult(True, True)
    
    