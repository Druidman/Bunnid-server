import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_user_sessions(connPool: asyncpg.Pool) -> DbResult:
    async with connPool.acquire() as conn:
        await conn.execute("""CREATE TABLE IF NOT EXISTS user_sessions(
                id SERIAL PRIMARY KEY,
                token TEXT UNIQUE,
                user_id INTEGER
            )"""
        )
    
    return DbResult[bool](result=True)
    
    