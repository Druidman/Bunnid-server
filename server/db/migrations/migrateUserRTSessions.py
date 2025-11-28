import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_user_RT_sessions(connPool: asyncpg.Pool) -> DbResult:
    async with connPool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS UserRTSessions(" \
                "id SERIAL PRIMARY KEY," \
                "token TEXT UNIQUE" \
            ")"
        )
  
    return DbResult(True, True)
    
    