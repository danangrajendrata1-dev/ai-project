import requests
TOKEN = None
BASE_URL = "http://127.0.0.1:8000"


def login_api(username, password):

    global TOKEN

    res = requests.post(
        "http://127.0.0.1:8000/auth/login",
        params={
            "username": username,
            "password": password
        }
    )

    data = res.json()

    if data["status"] == "success":
        TOKEN = data["access_token"]

    return data


def register_api(username, password):
    res = requests.post(
        f"{BASE_URL}/auth/register",
        params={
            "username": username,
            "password": password
        }
    )
    return res.json()


def send_message(session_id, message):
    res = requests.post(
        f"{BASE_URL}/chat/message",
        params={
            "session_id": session_id,
            "message": message
        }
    )
    return res.json()


def stream_message(session_id, message):

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    res = requests.get(
        "http://127.0.0.1:8000/chat/stream",
        params={
            "session_id": session_id,
            "message": message
        },
        headers=headers,
        stream=True
    )

    for chunk in res.iter_content(chunk_size=1024):
        if chunk:
            yield chunk.decode()