from .migrateUserSessions import *
from .migrateUsers import *
from .migrateUserRTSessions import *
from .migrateChatSystem import *
import asyncpg

async def migrate(connPool: asyncpg.Pool) -> bool:
    if (await migrate_user_sessions(connPool)).error:
        return False
    if (await migrate_user_RT_sessions(connPool)).error:
        return False
    if (await migrate_users(connPool)).error:
        return False
    if (await migrate_chat_system(connPool)).error:
        return False
    return True