from fastapi import FastAPI
from api.routes.auth import router as auth_router

app = FastAPI(
    title="AI Project API",
    version="1.0.0"
)

@app.get("/")
def home():

    return {
        "message": "AI Project API Running"
    }

app.include_router(auth_router, prefix="/auth")