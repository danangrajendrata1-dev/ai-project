from fastapi import FastAPI

from api.routes.auth import router as auth_router
# from api.routes.chat import router as chat_router

app = FastAPI(
    title="AI Project API",
    version="1.0.0"
)

# ROUTES
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(chat_router, prefix="/chat", tags=["Chat"])