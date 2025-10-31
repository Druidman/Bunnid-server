from flask import Blueprint
from server.httpServer.session.RTSession import make_RTS
from server import globals
from server.httpServer.auth.user_session import userSession
import server.globals as globals



session_bp = Blueprint("session", __name__)

@session_bp.route("/", methods=["GET"])
def main_route():
    return "<h1>Session Bunnid api</h1>"

@session_bp.route("/getRTS", methods=["POST"])
@userSession # validates userSession (user session token)
def get_realtime_session():
    rts_token: str = make_RTS()
    if (not rts_token):
        return globals.errors["FAILED_TO_ASSIGN_TOKEN"]
    
    return globals.API_RESPONSE(True, {"token":rts_token})



