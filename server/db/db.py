import asyncpg
import os
from .migrations import migrate


async def connectDb() ->  asyncpg.Pool | None:
    DATABASE_URL = os.getenv("BUNNID_DB_URL", "NONE")
    if DATABASE_URL == "NONE":
        return None
    pool:  asyncpg.Pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=5,
        max_size=20
    )
    
    
    if (await migrate(connPool=pool)):
        return pool
    else:
        return None



