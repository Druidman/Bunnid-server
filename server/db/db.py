import asyncpg

from .migrations import migrate


async def connectDb() ->  asyncpg.Pool | None:
    pool:  asyncpg.Pool = await asyncpg.create_pool(
        user="testUser",
        password="test",
        database="testDb",
        host='localhost',
        port=5432,
        min_size=5,
        max_size=20
    )
    
    
    if (await migrate(connPool=pool)):
        return pool
    else:
        return None



