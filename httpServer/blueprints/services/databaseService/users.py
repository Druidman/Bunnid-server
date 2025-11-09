from flask import Blueprint, request

from server import globals
from server.httpServer.auth.user_session import userSession
from server.db.tables.users import get_users_preview

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def usersMain():
    return "<h1>This is database/users api! (/get)</h1>"


@users_bp.route("/get", methods=["GET"])
@userSession
def usersGet():
    result = get_users_preview(100,db=globals.dbConn.cursor())
    return globals.api_response_from_db_response(result)
    