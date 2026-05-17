from fastapi import APIRouter
from models.session import Session
from fastapi import Depends
from core.dependencies import (
    get_current_user
)
from schemas.session_schema import (
    CreateSessionSchema
)

router = APIRouter()

session = Session()

# ======================
# GET ALL SESSIONS
# ======================
@router.get("/{user_id}")
def get_sessions(
    user_id: int,
    current_user: dict = Depends(
        get_current_user
    )
):

    data = session.get_all(user_id)

    return {
        "status": "success",
        "data": data
    }

# ======================
# CREATE SESSION
# ======================
@router.post("/create")
def create_session(
    data: CreateSessionSchema
):

    session_id = session.create(
        data.user_id
    )

    return {
        "status": "success",
        "session_id": session_id
    }

# ======================
# DELETE SESSION
# ======================
@router.delete("/{session_id}/{user_id}")
def delete_session(
    session_id: int,
    user_id: int
):

    session.delete(
        session_id,
        user_id
    )

    return {
        "status": "success"
    }