from fastapi import APIRouter
from models.chat import Chat

router = APIRouter()

chat = Chat()

# ======================
# LOAD CHAT HISTORY
# ======================
@router.get("/{session_id}")
def load_chat(session_id: int):

    data = chat.load(session_id)

    return {
        "status": "success",
        "data": data
    }

# ======================
# SAVE CHAT
# ======================
@router.post("/save")
def save_chat(data: dict):

    chat.save(
        data["session_id"],
        data["role"],
        data["message"]
    )

    return {
        "status": "success"
    }

# ======================
# CLEAR CHAT
# ======================
@router.delete("/{session_id}")
def clear_chat(session_id: int):

    chat.clear(session_id)

    return {
        "status": "success"
    }