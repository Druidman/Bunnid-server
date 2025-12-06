import datetime
from server.db.utils import DbResult
from typing import Optional
from server.db.tables.session_refresh_tokens import add_token_to_db
from fastapi import HTTPException
from .jwt import create_jwt
import server.globals as globals


async def create_session_refresh_token(user_id: int) -> str:
    if not user_id:
        return ""
    user_id = user_id
    created_at = datetime.datetime.now(datetime.timezone.utc)
    expires_at = created_at + datetime.timedelta(hours=globals.SESSION_REFRESH_TOKEN_EXPIRATION_HOURS)


    # make db entry
    result: DbResult[Optional[int]] = await add_token_to_db(
        user_id = user_id,
        created_at=created_at,
        expires_at=expires_at,
        connPool=globals.connPool
    )
    
    if result.error:
        raise HTTPException(status_code=500, detail=result.error)
    
    try:
        refresh_token: str = create_jwt(
            data={
                "user_id": str(user_id),
                "token_id": str(result.result)
            },
            expires_at=expires_at
        )
    except:
        # TODO add token removal (revoked=true) from db
        raise HTTPException(status_code=500, detail="Smth went wrong when making refresh token")
    
    return refresh_token