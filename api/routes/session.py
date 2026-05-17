from fastapi import APIRouter
from models.session import Session

router = APIRouter()

session = Session()

# ======================
# GET ALL SESSIONS
# ======================
@router.get("/{user_id}")
def get_sessions(user_id: int):

    data = session.get_all(user_id)

    return {
        "status": "success",
        "data": data
    }

# ======================
# CREATE SESSION
# ======================
@router.post("/create")
def create_session(data: dict):

    session_id = session.create(
        data["user_id"]
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