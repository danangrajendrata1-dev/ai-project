import os

from dotenv import load_dotenv

from jose import jwt, JWTError

from datetime import (
    datetime,
    timedelta
)

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ALGORITHM = "HS256"

# ======================
# CREATE TOKEN
# ======================
def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = (
        datetime.utcnow() +
        timedelta(days=1)
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# ======================
# VERIFY TOKEN
# ======================
def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None