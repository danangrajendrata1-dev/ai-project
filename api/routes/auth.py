from fastapi import APIRouter
from models.user import User

router = APIRouter()

user = User()

@router.post("/login")
def login(data: dict):

    result = user.login(
        data["username"],
        data["password"]
    )

    if result:

        return {
            "status": "success",
            "data": result
        }

    return {
        "status": "failed"
    }


@router.post("/register")
def register(data: dict):

    try:

        user.register(
            data["username"],
            data["password"]
        )

        return {
            "status": "success"
        }

    except:

        return {
            "status": "error"
        }