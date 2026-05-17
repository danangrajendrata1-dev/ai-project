from fastapi import Header, HTTPException

from core.security import (
    verify_token
)

# ======================
# GET CURRENT USER
# ======================
def get_current_user(
    authorization: str = Header(None)
):

    if authorization is None:

        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    try:

        token = authorization.split(" ")[1]

    except:

        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )

    payload = verify_token(token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload