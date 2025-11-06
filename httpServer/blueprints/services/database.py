
from flask import Blueprint, request

from server import globals


from .database import users_bp

database_bp = Blueprint("database", __name__)

database_bp.register_blueprint(users_bp, url_prefix="/users")


@database_bp.route("/", methods=["GET"])
def conversationMain():
    return "<h1>This is database api!</h1>"
