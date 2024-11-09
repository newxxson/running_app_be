# Define a user model
from uuid import UUID
from fastapi import HTTPException, Header
import jwt
from pydantic import BaseModel
from running_app.common.property.auth import auth_property


class TokenData(BaseModel):
    identifier: str | None = None


async def get_current_user(authorization: str | None = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Authorization header missing or malformed"
        )

    token = authorization.split(" ")[1]  # Extract the token part after "Bearer"

    try:
        # Decode the token
        payload = jwt.decode(
            token,
            auth_property.jwt_secret_key,
            algorithms=[auth_property.jwt_algorithm],
        )
        claims: dict | None = payload.get("claims")
        if claims is None or claims.get("user_identifier") is None:
            raise HTTPException(
                status_code=401, detail="User identifier missing in token"
            )
        return UUID(claims["user_identifier"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
