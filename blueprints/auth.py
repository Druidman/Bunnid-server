from flask import Blueprint


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def testRoute():
    return "<h1>Auth Bunnid API</h1>"



@auth_bp.route("/login")
def login():

    return "<h1>Auth Bunnid API Login</h1>"

@auth_bp.route("/reqister")
def register():
    return "<h1>Auth Bunnid API Register</h1>"



