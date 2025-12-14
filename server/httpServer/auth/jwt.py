import jwt
import datetime

def create_jwt(
        sub: str, 
        expires_at: datetime.datetime, 
        secret: str, 
        algorithm: str = "HS256", 
        additional_payload_data: dict[str,str] = None
) -> str | None: 
    payload = {
        "sub": sub,
        "exp": int(expires_at.timestamp())
    }
    
    if additional_payload_data:
        if "sub" in additional_payload_data or "exp" in additional_payload_data:
            raise ValueError("Cannot override sub or exp")
        payload.update(additional_payload_data)

    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token

def verify_jwt(jwt_token: str, secret: str, algorithms: list[str] = ["HS256"]) -> dict:
    try:
        decoded = jwt.decode(jwt_token, secret, algorithms=algorithms)
        return decoded
    except:
        raise
