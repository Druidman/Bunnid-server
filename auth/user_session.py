from flask import request

from ..globals import USER_TOKEN_LENGTH, dbConn, errors
from ..globals import dbConn
from ..db.tables.userSessions import check_if_token_in_db

def check_if_valid_token(token: str) -> bool:
    if (token == ""): return False
    if (len(token) < USER_TOKEN_LENGTH): return False

    return check_if_token_in_db(token, dbConn.cursor())




def userSession(func):
    def validate(*args, **kwargs):
        try:
            token = request.args.get("token")
            if (token == None):
                return errors["NO_ARGS"]
        except Exception as e:
            
            return errors["NO_ARGS"]
        
        if not check_if_valid_token(token):
            return errors['ACCES_DENIED']
        
        
        result = func()
        return result
    return validate