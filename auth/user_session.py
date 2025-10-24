from flask import request

from server import globals
from ..db.tables.userSessions import check_if_token_in_db

def check_if_valid_token(token: str) -> bool:
    if (token == ""): return False
    if (len(token) < globals.USER_TOKEN_LENGTH): return False

    return check_if_token_in_db(token, globals.dbConn.cursor())




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