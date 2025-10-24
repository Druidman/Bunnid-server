from flask import request
import secrets

from server import globals
from ..db.tables.userSessions import check_if_token_in_db, add_token_to_db

def check_if_valid_token(token: str) -> bool:
    if (token == ""): return False
    if (len(token) < globals.USER_TOKEN_LENGTH): return False

    return check_if_token_in_db(token, globals.dbConn.cursor())


def make_user_session() -> str:
    token: str = secrets.token_urlsafe(16)
    result = add_token_to_db(token=token, db=globals.dbConn.cursor())
    if not result["STATUS"]:
        print(f"Error when adding token: {result['MSG']}")
        return ""
    else:
        return token


def userSession(func):
    def validate(*args, **kwargs):
        try:
            token = request.args.get("token")
            if (token == None):
                return globals.errors["NO_ARGS"]
        except Exception as e:
            
            return globals.errors["NO_ARGS"]
        
        if not check_if_valid_token(token):
            return globals.errors['ACCES_DENIED']
        
        
        result = func()
        return result
    return validate