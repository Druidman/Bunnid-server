import asyncpg

from .migrations import migrate


async def connectDb() ->  asyncpg.Pool | None:
    pool:  asyncpg.Pool = await asyncpg.create_pool(
        user="testUser",
        password="test",
        database="testDb",
        port=5432,
        host="localhost",
        min_size=5,
        max_size=20
    )
    
    if (await migrate(connPool=pool)):
        return pool
    else:
        return None



