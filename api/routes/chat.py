from fastapi import APIRouter
from models.chat import Chat
from ai.engine import AIEngine
from core.security import verify_token
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from fastapi import WebSocket, WebSocketDisconnect
router = APIRouter()

chat = Chat()
ai = AIEngine()

@router.post("/message")
def chat_message(token: str, session_id: int, message: str):

    user = verify_token(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    chat.save(session_id, "user", message)

    history = chat.load(session_id)

    response = ai.ask(history)

    chat.save(session_id, "assistant", response)

    return {
        "response": response
    }

@router.get("/stream")
def stream_chat(token: str, session_id: int, message: str):

    user = verify_token(token)

    if not user:
        return {"error": "Unauthorized"}

    def generate():

        chat.save(session_id, "user", message)

        history = chat.load(session_id)

        full_response = ""

        for chunk in ai.stream(history):
            full_response += chunk
            yield chunk

        chat.save(session_id, "assistant", full_response)

    return StreamingResponse(generate(), media_type="text/plain")

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:

            data = await websocket.receive_json()

            token = data.get("token")
            session_id = data.get("session_id")
            message = data.get("message")

            # cek auth
            user = verify_token(token)

            if not user:
                await websocket.send_text("Unauthorized")
                continue

            # simpan user message
            chat.save(session_id, "user", message)

            history = chat.load(session_id)

            full_response = ""

            # streaming AI token per token
            for chunk in ai.stream(history):
                full_response += chunk
                await websocket.send_text(chunk)

            # simpan assistant
            chat.save(session_id, "assistant", full_response)

    except WebSocketDisconnect:
        print("Client disconnected")