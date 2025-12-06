import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def migrate_session_refresh_tokens(connPool: asyncpg.Pool) -> DbResult:
    async with connPool.acquire() as conn:
        await conn.execute("""CREATE TABLE IF NOT EXISTS session_refresh_tokens(
                id SERIAL PRIMARY KEY,
                           
                created_at TIMESTAMP,
                expires_at TIMESTAMP,
                           
                user_id INTEGER,
                           
                revoked BOOLEAN DEFAULT false
            )"""
        )
    
    return DbResult[bool](result=True)
    
    