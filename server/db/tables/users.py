import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def check_if_user_exists(login: str, password: str, db: sqlite3.Cursor) -> DbResult:
    if (not login or not password): return DbResult(False, "Incorrect login or password")
    
    db.execute("SELECT * FROM Users WHERE login=:login AND password=:password LIMIT 1",
               {
        
                    "login": login,
                    "password": password
                }
        )
    resRows = db.fetchone()
    if (resRows):
        return DbResult(True, True)
    else:
        return DbResult(True, False)

@dbFunction
def add_new_user(name: str, login: str, password: str, db: sqlite3.Cursor) -> DbResult:
    if (not name or not login or not password): return DbResult(False, "Wrong name or password or login")

    #check if exists
    nameResult: DbResult = get_user_by_name(name, db)
    loginResult: DbResult = get_user_by_login(login, db)
    if (not nameResult.status or not loginResult.status):
        return DbResult(False, f'NAME: {nameResult.msg} LOGIN: {loginResult.msg}')
    
    if (nameResult.msg):
        return DbResult(False, f"Account of this name already exists")
    
    if (loginResult.msg):
        return DbResult(False, f"Account of this login already exists")

    db.execute("INSERT INTO Users(name, login, password) VALUES(:name, :login, :password)", {
        "login": login,
        "name": name,
        "password": password
    })
    db.connection.commit()
    return DbResult(True, True)

@dbFunction
def get_user_by_name(name: str, db: sqlite3.Cursor)  -> DbResult:
    if (not name): return DbResult(False, "Wrong name")

    db.execute("SELECT id, name FROM Users WHERE name=:name LIMIT 1",{"name": name})
    resRows = db.fetchone()
    return DbResult(True, resRows, True)

@dbFunction
def get_user_by_login(login: str, db: sqlite3.Cursor) -> DbResult:
    if (not login): return DbResult(False, "Wrong login")

    db.execute("SELECT id, name FROM Users WHERE login=:login LIMIT 1",{"login": login})
    resRows = db.fetchone()
    return DbResult(True, resRows, True)

@dbFunction
def get_users_preview(limit: int, db: sqlite3.Cursor)  -> DbResult:
    if limit < 0: return DbResult(False, "Wrong limit")

    db.execute("SELECT id, name FROM Users LIMIT :limit", {"limit": limit})
    resRows = db.fetchall()
    return DbResult(True, resRows, True)