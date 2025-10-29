import sqlite3
from .migrations import migrate


def connectDb() -> sqlite3.Connection | None:
    dbConn = sqlite3.connect("database.db", check_same_thread=False)
    
    if (migrate(dbConn=dbConn)):
        return dbConn
    else:
        return None



