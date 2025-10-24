from flask import Blueprint


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def testRoute():
    return "<h1>Auth Bunnid API</h1>"



