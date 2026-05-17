from fastapi import APIRouter
from services.auth_service import (
    AuthService
)

from schemas.auth_schema import (
    LoginSchema,
    RegisterSchema
)
auth_service = AuthService()
router = APIRouter()

user = User()

@router.post("/login")
def login(data: LoginSchema):

    result = auth_service.login(
        data.username,
        data.password
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
def register(data: RegisterSchema):

    try:

        auth_service.register(
            data.username,
            data.password
        )

        return {
            "status": "success"
        }

    except:

        return {
            "status": "error"
        }