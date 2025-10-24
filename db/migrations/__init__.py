from .migrateUserSessions import *
import sqlite3

def migrate(dbConn: sqlite3.Connection) -> bool:
    if not migrate_user_sessions(dbConn.cursor()):
        return False
    return True