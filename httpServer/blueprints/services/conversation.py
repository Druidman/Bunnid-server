from flask import Blueprint, request
from server.httpServer.auth import userSession

from server import globals

conversation_bp = Blueprint("conversation", __name__)


@conversation_bp.route("/", methods=["GET"])
def conversationMain():
    return "<h1>This is conversation api! /message, /get</h1>"


@conversation_bp.route("/send", methods=["POST"])
@userSession
def conversationMain(): pass


@conversation_bp.route("/get", methods=["POST"])
@userSession
def conversationMain():
    try:
        conversationId = request.json.get("conversationId")
    except:
        return globals.errors["NO_ARGS"]
    
    




