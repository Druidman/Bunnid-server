from .db import connectDb
from .tables.conversation_members import add_member, get_members
from .tables.conversations import add_conversation, get_conversation, get_conversation_by_title, get_conversations
from .tables.messages import add_message, get_message, get_messages
from .tables.userRTSessions import add_token_to_db, check_if_token_in_db
from .tables.users import add_new_user, get_user_by_login, get_user_by_name, get_users_preview, check_if_user_exists
from .tables.userSessions import add_token_to_db, check_if_token_in_db, get_token_data

import asyncpg

async def conversation_members_test(connPool):
    try:
        if not await add_member(1, connPool).status:
            print("add_member NOT PASSED")
            return
        
    except:
        print("conversation_members_test NOT PASSED")
    
async def conversations_test(connPool): pass
async def messages_test(connPool): pass
async def userRTSessions_test(connPool): pass
async def users_test(connPool): pass
async def userSessions_test(connPool): pass

async def main():
    connPool = await connectDb()
    # now tests
    print("db set up PASSED")

    print("STARTING TESTS")

    await conversation_members_test(connPool)
    await conversations_test(connPool)
    await messages_test(connPool)
    await userRTSessions_test(connPool)
    await users_test(connPool)
    await userSessions_test(connPool)

    print("TESTS ENDED")
