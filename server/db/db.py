import asyncpg

from .migrations import migrate


async def connectDb() ->  asyncpg.Pool | None:
    pool:  asyncpg.Pool = await asyncpg.create_pool(
        user="bunnidAdmin",
        password="nimda",
        database="bunnidDb",
        host='localhost',
        port=5432,
        min_size=5,
        max_size=20
    )
    
    
    if (await migrate(connPool=pool)):
        return pool
    else:
        return None



