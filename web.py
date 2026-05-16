import streamlit as st

# =====================
# OOP IMPORTS
# =====================
from models.user import User
from models.session import Session
from models.chat import Chat
from ai.engine import AIEngine

# =====================
# INIT OBJECTS
# =====================
user = User()
session = Session()
chat = Chat()
ai = AIEngine()

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="AI TKJ Assistant",
    layout="centered"
)

st.title("🤖 AI TKJ Assistant")

# =====================
# SESSION STATE INIT
# =====================
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================
# AUTH SYSTEM
# =====================
if st.session_state.user_id is None:

    st.title("🔐 Login System")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ========== LOGIN ==========
    with tab1:

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):

            user_id = user.login(username, password)

            if user_id:

                st.session_state.user_id = user_id
                st.success("Login berhasil")
                st.rerun()

            else:
                st.error("Login gagal")

    # ========== REGISTER ==========
    with tab2:

        r_username = st.text_input("Username Baru", key="reg_user")
        r_password = st.text_input("Password Baru", type="password", key="reg_pass")

        if st.button("Register"):

            try:
                user.register(r_username, r_password)
                st.success("Register berhasil, silakan login")

            except:
                st.error("Username sudah digunakan")

    st.stop()

# =====================
# LOAD SESSION
# =====================
if st.session_state.current_session is None:

    sessions = session.get_all(st.session_state.user_id)

    if not sessions:

        session_id = session.create(st.session_state.user_id)
        st.session_state.current_session = session_id

    else:
        st.session_state.current_session = sessions[0][0]

# =====================
# LOAD CHAT HISTORY
# =====================
if len(st.session_state.messages) == 0:

    history = chat.load(st.session_state.current_session)
    st.session_state.messages.extend(history)

# =====================
# SHOW CHAT HISTORY
# =====================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# =====================
# USER INPUT
# =====================
user_input = st.chat_input("Tulis pesan...")

if user_input:

    # auto title
    if len(st.session_state.messages) <= 1:

        title = user_input[:30]

        session.update_title(
            st.session_state.current_session,
            st.session_state.user_id,
            title
        )

    # show user
    with st.chat_message("user"):
        st.write(user_input)

    # save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    chat.save(
        st.session_state.current_session,
        "user",
        user_input
    )

    # AI RESPONSE
    recent_messages = st.session_state.messages

    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        stream = ai.stream(recent_messages)

        for chunk in stream:

            content = chunk["message"]["content"]
            full_response += content
            placeholder.markdown(full_response)

    ai_reply = full_response

    # save AI message
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    chat.save(
        st.session_state.current_session,
        "assistant",
        ai_reply
    )

# =====================
# SIDEBAR
# =====================
with st.sidebar:

    st.title("💬 Sessions")

    # logout
    if st.button("🚪 Logout"):
        st.session_state.user_id = None
        st.session_state.messages = []
        st.session_state.current_session = None
        st.rerun()

    # new chat
    if st.button("➕ New Chat"):

        session_id = session.create(st.session_state.user_id)
        st.session_state.current_session = session_id
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # list sessions
    sessions = session.get_all(st.session_state.user_id)

    for s in sessions:

        session_id = s[0]
        title = s[1]

        col1, col2 = st.columns([4, 1])

        with col1:

            if st.button(
                f"📌 {title}",
                key=f"session_{session_id}"
            ):

                st.session_state.current_session = session_id
                st.session_state.messages = chat.load(session_id)
                st.rerun()

        with col2:

            if st.button(
                "❌",
                key=f"delete_{session_id}"
            ):

                session.delete(
                    session_id,
                    st.session_state.user_id
                )

                st.session_state.messages = []

                sessions = session.get_all(st.session_state.user_id)

                if sessions:
                    st.session_state.current_session = sessions[0][0]
                else:
                    new_id = session.create(st.session_state.user_id)
                    st.session_state.current_session = new_id

                st.rerun()