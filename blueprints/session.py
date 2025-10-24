from flask import Blueprint, request


from ..globals import errors, API_RESPONSE
from ..auth.user_session import userSession



session_bp = Blueprint("session", __name__)

@session_bp.route("/", methods=["GET"])
def main_route():
    return "<h1>Session Bunnid api</h1>"

@session_bp.route("/getRTS", methods=["GET"])
@userSession
def get_realtime_session():
    return API_RESPONSE(True, "Work in progress endpoint")



