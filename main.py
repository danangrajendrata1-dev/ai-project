from fastapi import FastAPI

from api.routes.auth import (
    router as auth_router
)

from api.routes.session import (
    router as session_router
)

from api.routes.chat import (
    router as chat_router
)

app = FastAPI(
    title="AI Project API",
    version="1.0.0"
)

@app.get("/")
def home():

    return {
        "message": "AI Project API Running"
    }

app.include_router(
    auth_router,
    prefix="/auth"
)

app.include_router(
    session_router,
    prefix="/session"
)

app.include_router(
    chat_router,
    prefix="/chat"
)