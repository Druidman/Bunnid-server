import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def check_if_user_exists(login: str, password: str, db: sqlite3.Cursor) -> dict:
    if (not login or not password): return DB_RESULT(False, "Incorrect login or password")
    
    db.execute("SELECT * FROM Users WHERE login=:login AND password=:password LIMIT 1",
               {
        
                    "login": login,
                    "password": password
                }
        )
    resRows = db.fetchone()
    if (resRows):
        return DB_RESULT(True, True)
    else:
        return DB_RESULT(True, False)

@dbFunction
def add_new_user(name: str, login: str, password: str, db: sqlite3.Cursor) -> dict:
    if (not name or not login or not password): return DB_RESULT(False, "Wrong name or password or login")

    #check if exists
    nameResult = get_user_by_name(name, db)
    loginResult = get_user_by_login(login, db)
    if (not nameResult["STATUS"] or not loginResult["STATUS"]):
        return DB_RESULT(False, f'NAME: {nameResult["MSG"]} LOGIN: {loginResult["MSG"]}')
    
    if (nameResult["MSG"]):
        return DB_RESULT(False, f"Account of this name already exists")
    
    if (loginResult["MSG"]):
        return DB_RESULT(False, f"Account of this login already exists")

    db.execute("INSERT INTO Users(name, login, password) VALUES(:name, :login, :password)", {
        "login": login,
        "name": name,
        "password": password
    })
    db.connection.commit()
    return DB_RESULT(True, True)

@dbFunction
def get_user_by_name(name: str, db: sqlite3.Cursor)  -> dict:
    if (not name): return DB_RESULT(False, "Wrong name")

    db.execute("SELECT * FROM Users WHERE name=:name LIMIT 1",{"name": name})
    resRows = db.fetchone()
    return DB_RESULT(True, resRows)

@dbFunction
def get_user_by_login(login: str, db: sqlite3.Cursor) -> dict:
    if (not login): return DB_RESULT(False, "Wrong login")

    db.execute("SELECT * FROM Users WHERE login=:login LIMIT 1",{"login": login})
    resRows = db.fetchone()
    return DB_RESULT(True, resRows)

@dbFunction
def get_users_preview(limit: int, db: sqlite3.Cursor)  -> dict:
    if limit < 0: return DB_RESULT(False, "Wrong limit")

    db.execute("SELECT name FROM Users")
    resRows = db.fetchall()
    return DB_RESULT(True, resRows)