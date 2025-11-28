import asyncpg
from ..utils import DbResult, dbFunction

@dbFunction
async def check_if_user_exists(login: str, password: str, connPool: asyncpg.Pool) -> DbResult:
    if (not login or not password): return DbResult(False, "Incorrect login or password")
    
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM Users WHERE login=:login AND password=:password LIMIT 1",
                {
            
                        "login": login,
                        "password": password
                    }
            )
    
    if (row):
        return DbResult(True, True)
    else:
        return DbResult(True, False)

@dbFunction
async def get_full_user(login: str, password: str, connPool: asyncpg.Pool) -> DbResult:
    if (not login or not password): return DbResult(False, "Incorrect login or password")
    
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM Users WHERE login=:login AND password=:password LIMIT 1",
                {
            
                    "login": login,
                    "password": password
                }
            )
    
    if (row):
        return DbResult(True, row)
    else:
        return DbResult(True, "")

@dbFunction
async def add_new_user(name: str, login: str, password: str, connPool: asyncpg.Pool) -> DbResult:
    if (not name or not login or not password): return DbResult(False, "Wrong name or password or login")

    #check if exists
    nameResult: DbResult = await get_user_by_name(name, connPool)
    loginResult: DbResult = await get_user_by_login(login, connPool)
    if (not nameResult.status or not loginResult.status):
        return DbResult(False, f'NAME: {nameResult.msg} LOGIN: {loginResult.msg}')
    
    if (nameResult.msg):
        return DbResult(False, f"Account of this name already exists")
    
    if (loginResult.msg):
        return DbResult(False, f"Account of this login already exists")
    
    async with connPool.acquire() as conn:
        await conn.execute("INSERT INTO Users(name, login, password) VALUES(:name, :login, :password)", {
            "login": login,
            "name": name,
            "password": password
        })
    
    return DbResult(True, True)

@dbFunction
async def get_user_by_name(name: str, connPool: asyncpg.Pool)  -> DbResult:
    if (not name): return DbResult(False, "Wrong name")

    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name FROM Users WHERE name=:name LIMIT 1",{"name": name})
    
    return DbResult(True, row, True)

@dbFunction
async def get_user_by_login(login: str, connPool: asyncpg.Pool) -> DbResult:
    if (not login): return DbResult(False, "Wrong login")
    async with connPool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name FROM Users WHERE login=:login LIMIT 1",{"login": login})
    
    return DbResult(True, row, True)

@dbFunction
async def get_users_preview(limit: int, connPool: asyncpg.Pool)  -> DbResult:
    if limit < 0: return DbResult(False, "Wrong limit")
    async with connPool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM Users LIMIT :limit", {"limit": limit})
    
    return DbResult(True, rows, True)