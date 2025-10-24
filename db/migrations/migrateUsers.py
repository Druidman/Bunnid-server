import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def migrate_users(db: sqlite3.Cursor) -> dict:
    db.execute("CREATE TABLE IF NOT EXISTS Users(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "name TEXT," \
            "login TEXT," \
            "password TEXT," \
            "unique(name, login)" \
            
        ")"
    )
    db.connection.commit()
    return DB_RESULT(True, True)
    
    