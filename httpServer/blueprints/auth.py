from flask import Blueprint, request
from server.db.tables.users import check_if_user_exists, add_new_user
from ..auth import make_user_session

from server import globals

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def testRoute():
    return "<h1>Auth Bunnid API</h1>"



@auth_bp.route("/login", methods=["POST"])
def login():
    login: str | None = request.json.get("login")
    password: str | None = request.json.get("password")
    if (not login or not password):
        return globals.API_RESPONSE(False, "Password, name, login not provided")
    
    res = check_if_user_exists( login, password, globals.dbConn.cursor())
    if (not res["STATUS"]):
        return globals.errors["LOGIN_TRY_AGAIN"]
    else:
        if (not res["MSG"]):
            return globals.errors["INCORRECT_LOGIN_VALUES"]
        token = make_user_session()
        if not token:

            return globals.errors("FAILED_TO_ASSIGN_TOKEN")
        else:
            return globals.API_RESPONSE(True, {"token": token})


@auth_bp.route("/register", methods=["POST"])
def register():
    name: str | None = request.json.get("name")
    login: str | None = request.json.get("login")
    password: str | None = request.json.get("password")
    if (not name or not login or not password):
        return globals.API_RESPONSE(False, "Password, name, login not provided")
    
    res = add_new_user(name, login, password, globals.dbConn.cursor())
    
    return globals.API_RESPONSE(res["STATUS"], res["MSG"])


