from flask import request
import secrets

from server import globals
from server.db.tables.userSessions import check_if_token_in_db, add_token_to_db
from server.db.utils import DbResult

def check_if_valid_token(token: str) -> bool:
    if (token == ""): return False
    if (len(token) < globals.USER_TOKEN_LENGTH): return False

    result: DbResult = check_if_token_in_db(token, globals.dbConn.cursor())
    if not result.status:
        return False
    return result.msg

def make_user_session(userId: str) -> str:
    token: str = secrets.token_urlsafe(globals.USER_TOKEN_LENGTH)
    result: DbResult = add_token_to_db(token=token, userId=userId, db=globals.dbConn.cursor())
    if not result.status:
        print(f"Error when adding token: {result.msg}")
        return ""
    else:
        return token


def userSession(func):
    def validateToken(*args, **kwargs):
        try:
            token = request.json.get("token")
            if (token == None):
                return globals.errors["NO_ARGS"]
        except Exception as e:
            
            return globals.errors["NO_ARGS"]
        
        if not check_if_valid_token(token):
            return globals.errors['ACCES_DENIED']
        
        
        result = func()
        return result
    
    validateToken.__name__ = func.__name__
    return validateToken