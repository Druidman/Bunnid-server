from flask import Blueprint, request
from ..db.tables.users import add_new_user

from server import globals

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def testRoute():
    return "<h1>Auth Bunnid API</h1>"



@auth_bp.route("/login")
def login():

    return "<h1>Auth Bunnid API Login</h1>"

@auth_bp.route("/register", methods=["GET"]) # FIX TO PUT
def register():
    name: str | None = request.args.get("name") 
    login: str | None = request.args.get("login")
    password: str | None = request.args.get("password")
    if (not name or not login or not password):
        return globals.API_RESPONSE(False, "Password, name, login not provided")
    
    res = add_new_user(name, login, password, globals.dbConn.cursor())
    
    return globals.API_RESPONSE(res["STATUS"], res["MSG"])


