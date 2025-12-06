from .migrateSessionRefreshTokens import *
from .migrateUsers import *
from .migrateChatSystem import *
import asyncpg

async def migrate(connPool: asyncpg.Pool) -> bool:
    if (await migrate_session_refresh_tokens(connPool)).error:
        return False
    if (await migrate_users(connPool)).error:
        return False
    if (await migrate_chat_system(connPool)).error:
        return False
    return True