from .migrateUserSessions import *
from .migrateUsers import *
from .migrateUserRTSessions import *
from .migrateChatSystem import *
import sqlite3

def migrate(dbConn: sqlite3.Connection) -> bool:
    if not migrate_user_sessions(dbConn.cursor()):
        return False
    if not migrate_user_RT_sessions(dbConn.cursor()):
        return False
    if not migrate_users(dbConn.cursor()):
        return False
    if not migrate_chat_system(dbConn.cursor()):
        return False
    return True