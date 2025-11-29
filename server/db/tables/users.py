import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def check_if_user_exists(login: str, password: str, connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if (not login or not password): return DbResult[None](error="Incorrect login or password")
    
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE login=$1 AND password=$1 LIMIT 1",
            login,
            password
        )
    
    if (row):
        return DbResult[bool](result=True)
    else:
        return DbResult[bool](result=False)

@dbFunction
async def get_full_user(login: str, password: str, connPool: asyncpg.Pool) -> DbResult[None | asyncpg.Record]:
    if (not login or not password): return DbResult[None](error="Incorrect login or password")
    
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE login=$1 AND password=$2 LIMIT 1",
            login,
            password
        )
    
    if (row):
        return DbResult[asyncpg.Record](result=row)
    else:
        return DbResult[None](error="Incorrect login or password. User not found")

@dbFunction
async def add_new_user(name: str, login: str, password: str, connPool: asyncpg.Pool) -> DbResult[None | bool]:
    if (not name or not login or not password): return DbResult[None](error="Wrong name or password or login")

    # check if exists
    nameResult: DbResult = await get_user_by_name(name, connPool)
    loginResult: DbResult = await get_user_by_login(login, connPool)
    if (not nameResult.status or not loginResult.status):
        return DbResult[None](error=f'NAME: {nameResult.msg} LOGIN: {loginResult.msg}')
    
    if (nameResult.msg):
        return DbResult[None](error=f"Account of this name already exists")
    
    if (loginResult.msg):
        return DbResult[None](error=f"Account of this login already exists")
    
    async with connPool.acquire() as conn:
        await conn.execute("INSERT INTO Users(name, login, password) VALUES($1, $2, $3)", 
            name,
            login,
            password
        )
    
    return DbResult[bool](result=True)

@dbFunction
async def get_user_by_name(name: str, connPool: asyncpg.Pool)  -> DbResult[None | asyncpg.Record]:
    if (not name): return DbResult[None](error="Wrong name")

    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name FROM Users WHERE name=$1 LIMIT 1",name)
    
    return DbResult[asyncpg.Record](result=row)

@dbFunction
async def get_user_by_login(login: str, connPool: asyncpg.Pool) -> DbResult[None | asyncpg.Record]:
    if (not login): return DbResult[None](error="Wrong login")
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name FROM Users WHERE login=$1 LIMIT 1",login)
    
    return DbResult[asyncpg.Record](result=row)

@dbFunction
async def get_users_preview(limit: int, connPool: asyncpg.Pool)  -> DbResult[None | list[asyncpg.Record]]:
    if limit < 0: return DbResult[None](error="Wrong limit")
    async with connPool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM Users LIMIT $1",limit)
    
    return DbResult[list[asyncpg.Record]](result=rows)