import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_user_RT_sessions(connPool: asyncpg.Pool) -> DbResult:
    async with connPool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS UserRTSessions(" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "token TEXT," \
                "unique(token)" \
            ")"
        )
  
    return DbResult(True, True)
    
    