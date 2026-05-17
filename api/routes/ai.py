from fastapi import APIRouter
from schemas.ai_schema import (
    AIChatSchema
)


router = APIRouter()

# ======================
# AI CHAT
# ======================
@router.post("/chat")
def ai_chat(
    data: AIChatSchema
):

    user_message = data.message

    ai_response = (
        f"AI menerima pesan: {user_message}"
    )

    return {
        "status": "success",
        "response": ai_response
    }