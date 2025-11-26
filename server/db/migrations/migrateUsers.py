import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_users(connPool: asyncpg.Pool) -> DbResult:
    async with connPool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS Users(" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "name TEXT," \
                "login TEXT," \
                "password TEXT," \
                "unique(name, login)" \
                
            ")"
        )
    
    return DbResult(True, True)
    
    