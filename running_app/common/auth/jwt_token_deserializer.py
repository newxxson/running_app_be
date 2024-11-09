# Define a user model
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
        user_identifier: str | None = payload.get("sub")
        if user_identifier is None:
            raise HTTPException(
                status_code=401, detail="User identifier missing in token"
            )
        return {"user_identifier": user_identifier}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
