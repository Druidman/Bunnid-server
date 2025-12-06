import jwt
import datetime

def create_jwt(data: dict, expires_at: datetime.datetime, secret: str, algorithm: str = "HS256") -> str | None:
    if not isinstance(data, dict):
        return None
    
    payload = {
        "sub": data,
        "exp": int(expires_at.timestamp())
    }
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token

def verify_jwt(jwt_token: str, secret: str, algoritms: list[str] = ["HS256"]) -> dict:
    try:
        decoded = jwt.decode(jwt_token, secret, algorithms=algoritms)
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
