from fastapi import APIRouter
from models.user import User

router = APIRouter()
user = User()

@router.post("/login")
def login(username: str, password: str):

    user_id = user.login(username, password)

    if user_id:
        return {
            "status": "success",
            "user_id": user_id
        }

    return {
        "status": "failed"
    }


@router.post("/register")
def register(username: str, password: str):

    try:
        user.register(username, password)
        return {"status": "success"}

    except:
        return {"status": "error"}