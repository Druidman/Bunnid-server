import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_users(connPool: asyncpg.Pool) -> DbResult:
    async with connPool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS Users(" \
                "id SERIAL PRIMARY KEY," \
                "name TEXT UNIQUE," \
                "login TEXT UNIQUE," \
                "password TEXT," \

            ")"
        )
    
    return DbResult(True, True)
    
    