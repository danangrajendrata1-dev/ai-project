import asyncio
import websockets
import json

async def stream_ws(token, session_id, message, callback):

    uri = "ws://127.0.0.1:8000/chat/ws/chat"

    async with websockets.connect(uri) as websocket:

        await websocket.send(json.dumps({
            "token": token,
            "session_id": session_id,
            "message": message
        }))

        full_response = ""

        while True:

            try:
                chunk = await websocket.recv()
                full_response += chunk

                callback(full_response)

            except:
                break

        return full_response