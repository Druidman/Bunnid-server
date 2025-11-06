from flask import Blueprint, request
from server.httpServer.auth import userSession
from server.db.tables.conversations import get_conversation, add_conversation
from server.db.tables.messages import get_messages, add_message

from server import globals

conversation_bp = Blueprint("conversation", __name__)


@conversation_bp.route("/", methods=["GET"])
def conversationMain():
    return "<h1>This is conversation api! /message, /get</h1>"


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

    if (not result["STATUS"]):
        return globals.API_RESPONSE(False, result["MSG"])
    
    return globals.API_RESPONSE(True, result["MSG"])

@conversation_bp.route("/getMessages", methods=["POST"])
@userSession
def conversationGetMessages():
    try:
        conversationId = request.json.get("conversationId")
    except:
        return globals.errors["NO_ARGS"]
    
    result = get_messages(convId=conversationId, db=globals.dbConn.cursor())

    if (not result["STATUS"]):
        return globals.API_RESPONSE(False, result["MSG"])
    
    return globals.API_RESPONSE(True, result["MSG"])


@conversation_bp.route("/create", methods=["POST"])
@userSession
def conversationCreate():
    try:
        conversationTitle = request.json.get("conversationTitle")
    except:
        return globals.errors["NO_ARGS"]
    
    result = add_conversation(title=conversationTitle, db=globals.dbConn.cursor())

    if (not result["STATUS"]):
        return globals.API_RESPONSE(False, result["MSG"])
    
    return globals.API_RESPONSE(True, result["MSG"])
    
@conversation_bp.route("/get", methods=["POST"])
@userSession
def conversationGet():
    try:
        conversationId = request.json.get("conversationId")
    except:
        return globals.errors["NO_ARGS"]
    
    conversation = get_conversation(convId=conversationId, db=globals.dbConn.cursor())

    if (not conversation["STATUS"]):
        return globals.API_RESPONSE(False, conversation["MSG"])
    
    return globals.API_RESPONSE(True, conversation["MSG"])


    

    
    




