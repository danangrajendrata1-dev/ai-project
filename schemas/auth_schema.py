from pydantic import BaseModel

# ======================
# LOGIN
# ======================
class LoginSchema(BaseModel):

    username: str
    password: str

# ======================
# REGISTER
# ======================
class RegisterSchema(BaseModel):

    username: str
    password: str