from pydantic import BaseModel

# ======================
# CREATE SESSION
# ======================
class CreateSessionSchema(BaseModel):

    user_id: int

# ======================
# DELETE SESSION
# ======================
class DeleteSessionSchema(BaseModel):

    session_id: int
    user_id: int