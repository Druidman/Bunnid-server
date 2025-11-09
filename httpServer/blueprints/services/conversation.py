from flask import Blueprint, request
from server.httpServer.auth.user_session import userSession
from server.db.tables.conversations import get_conversation, add_conversation, get_conversations
from server.db.tables.messages import get_messages, add_message
from server.db.tables.conversation_members import add_member, get_members

from server import globals
from server.db.utils import DbResult

conversation_bp = Blueprint("conversation", __name__)


@conversation_bp.route("/", methods=["GET"])
def conversationMain():
    return "<h1>This is conversation api!</h1>"


@conversation_bp.route("/send", methods=["POST"])
@userSession
def conversationSendMsg():
    try:
        conversationId = request.json.get("conversationId")
        msgContent = request.json.get("msgContent")
        userId = request.json.get("userId")
    except:
        return globals.errors["NO_ARGS"]
    
    result = add_message(convId=conversationId, userId=userId, content=msgContent, db=globals.dbConn.cursor())
    return globals.api_response_from_db_repsonse(result)
  

@conversation_bp.route("/getMessages", methods=["POST"])
@userSession
def conversationGetMessages():
    try:
        conversationId = request.json.get("conversationId")
    except:
        return globals.errors["NO_ARGS"]
    
    result = get_messages(convId=conversationId, limit=100, db=globals.dbConn.cursor())

    return globals.api_response_from_db_repsonse(result)


@conversation_bp.route("/create", methods=["POST"])
@userSession
def conversationCreate():
    try:
        conversationTitle = request.json.get("conversationTitle")
    except:
        return globals.errors["NO_ARGS"]
    
    result = add_conversation(title=conversationTitle, db=globals.dbConn.cursor())

    return globals.api_response_from_db_repsonse(result)


@conversation_bp.route("/addMember", methods=["POST"])
@userSession
def conversationAddMember():
    try:
        conversationId = request.json.get("conversationId")
        memberId = request.json.get("memberId")
    except:
        return globals.errors["NO_ARGS"]
    
    result = add_member(convId=conversationId, userId=memberId, db=globals.dbConn.cursor())

    return globals.api_response_from_db_repsonse(result)

@conversation_bp.route("/getMembers", methods=["POST"])
@userSession
def conversationGetMembers():
    try:
        conversationId = request.json.get("conversationId")
    except:
        return globals.errors["NO_ARGS"]
    
    result = get_members(convId=conversationId, db=globals.dbConn.cursor())

    return globals.api_response_from_db_repsonse(result)
    
@conversation_bp.route("/get", methods=["POST"])
@userSession
def conversationGet():
    try:
        conversationId = request.json.get("conversationId")
    except:
        return globals.errors["NO_ARGS"]
    
    result = get_conversation(convId=conversationId, db=globals.dbConn.cursor())

    return globals.api_response_from_db_repsonse(result)


@conversation_bp.route("/list", methods=["POST"])
@userSession
def conversationList():
    
    result: DbResult = get_conversations(limit=100, db=globals.dbConn.cursor())
    return globals.api_response_from_db_repsonse(result)


    

    
    




