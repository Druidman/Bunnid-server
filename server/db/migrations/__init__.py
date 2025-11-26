from .migrateUserSessions import *
from .migrateUsers import *
from .migrateUserRTSessions import *
from .migrateChatSystem import *
import asyncpg

async def migrate(connPool: asyncpg.Pool) -> bool:
    if not await migrate_user_sessions(connPool):
        return False
    if not await migrate_user_RT_sessions(connPool):
        return False
    if not await migrate_users(connPool):
        return False
    if not await migrate_chat_system(connPool):
        return False
    return True