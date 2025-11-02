from flask import Blueprint, request

from server import globals

conversation_bp = Blueprint("conversation", __name__)


@conversation_bp.route("/", methods=["GET"])
def conversationMain():
    return "<h1>This is conversation api! /message, /get</h1>"




