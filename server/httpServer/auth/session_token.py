import datetime
from typing import Annotated
from fastapi import HTTPException, Header
from .jwt import create_jwt, verify_jwt
import server.globals as globals


async def verify_session_token(session_token: str) -> dict:
    payload: dict = verify_jwt(
        jwt_token=session_token, 
        secret=globals.SESSION_TOKEN_SECRET_KEY,
        algorithms=[globals.SESSION_TOKEN_ALGORITHM]
    )
    
    if not payload:
        raise HTTPException(status_code=406, detail="No payload in token found")
    
    return payload


async def verify_session_token_header(authorization: Annotated[str | None, Header()]) -> dict:
    if not authorization:
        raise HTTPException(status_code=406, detail="No token found") 
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=406, detail="Invalid authorization header form") 
    
    session_token: str = authorization[len("Bearer "):]
    print(f"Token: {session_token}")
    return await verify_session_token(session_token=session_token)


async def create_session_token(user_id: int) -> str:
    if not user_id:
        return ""
    
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=globals.SESSION_TOKEN_EXPIRY_MINUTES)

    try:
        session_token: str = create_jwt(
            sub=str(user_id),
            expires_at=expires_at,
            algorithm=globals.SESSION_TOKEN_ALGORITHM
        )
    except:
        # TODO add token removal (revoked=true) from db
        raise HTTPException(status_code=500, detail="Smth went wrong when making session token")
    
    return session_token