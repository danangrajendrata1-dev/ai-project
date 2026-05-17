from pydantic import BaseModel

# ======================
# SAVE CHAT
# ======================
class SaveChatSchema(BaseModel):

    session_id: int
    role: str
    message: str