import requests
TOKEN = None

BASE_URL = "http://ai-project-production-0626.up.railway.app"


def login(username, password):

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    return response.json()


def register(username, password):

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": username,
            "password": password
        }
    )

    return response.json()


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

# ======================
# GET SESSIONS
# ======================
def get_sessions(user_id):

    response = requests.get(
        f"{BASE_URL}/session/{user_id}"
    )

    return response.json()

# ======================
# CREATE SESSION
# ======================
def create_session(user_id):

    response = requests.post(
        f"{BASE_URL}/session/create",
        json={
            "user_id": user_id
        }
    )

    return response.json()

# ======================
# DELETE SESSION
# ======================
def delete_session(
    session_id,
    user_id
):

    response = requests.delete(
        f"{BASE_URL}/session/{session_id}/{user_id}"
    )

    return response.json()