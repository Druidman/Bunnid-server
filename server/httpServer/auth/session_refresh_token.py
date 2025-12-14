import datetime
from server.db.utils import DbResult
from typing import Optional
from server.db.tables.session_refresh_tokens import add_token_to_db, check_if_token_revoked
from fastapi import HTTPException, Cookie
from .jwt import create_jwt, verify_jwt
import jwt
import server.globals as globals

async def verify_session_refresh_token(session_refresh_token: str) -> dict:
    print(f"Session refresh token: {session_refresh_token}")
    try:
        payload: dict = verify_jwt(
            jwt_token=session_refresh_token, 
            secret=globals.SESSION_REFRESH_TOKEN_SECRET_KEY,
            algorithms=[globals.SESSION_REFRESH_TOKEN_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalid")
    except:
        raise HTTPException(status_code=401, detail="Token validation went wrong")

    
    if not payload:
        raise HTTPException(status_code=406, detail="No payload in token found")
    
    # now that it is verified that token has been created on server and is authentic we can check if is revoked
    result: DbResult[Optional[bool]] = await check_if_token_revoked(payload.get("token_id"), connPool=globals.connPool)

    if result.error:
        raise HTTPException(status_code=500, detail=result.error)
    
    if result.result:
        raise HTTPException(status_code=401, detail="Not valid token")
    
    return payload

async def verify_session_refresh_token_cookie(session_refresh_token: str = Cookie(None)) -> dict:
    try:
        res = verify_session_refresh_token(session_refresh_token=session_refresh_token)
        return res
    except:
        raise

async def create_session_refresh_token(user_id: int) -> str:
    if not user_id:
        return ""
    user_id = user_id
    created_at = datetime.datetime.now(datetime.timezone.utc)
    expires_at = created_at + datetime.timedelta(hours=globals.SESSION_REFRESH_TOKEN_EXPIRY_HOURS)


    # make db entry
    result: DbResult[Optional[int]] = await add_token_to_db(
        user_id = user_id,
        created_at=created_at.date(),
        expires_at=expires_at.date(),
        connPool=globals.connPool
    )
    
    if result.error:
        raise HTTPException(status_code=500, detail=result.error)
    
    try:
        refresh_token: str = create_jwt(
            sub=str(user_id),
            expires_at=expires_at,
            algorithm=globals.SESSION_REFRESH_TOKEN_ALGORITHM,
            secret=globals.SESSION_REFRESH_TOKEN_SECRET_KEY,
            additional_payload_data={
                "token_id": str(result.result)
            }
        )
    except Exception as e:
        # TODO add token removal (revoked=true) from db
        raise HTTPException(status_code=500, detail=f"Smth went wrong when making refresh token: {e}")
    
    return refresh_token


