import streamlit as st

from services.api_client import (
    login,
    register,
    get_sessions,
    create_session,
    delete_session,
    load_chat,
    save_chat,
    clear_chat,
    ai_chat
)

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="AI Project",
    layout="centered"
)

st.title("🤖 AI Project")

# =====================
# SESSION STATE
# =====================
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================
# LOGIN / REGISTER
# =====================
if st.session_state.user_id is None:

    st.title("🔐 Login System")

    tab1, tab2 = st.tabs([
        "Login",
        "Register"
    ])

    # =====================
    # LOGIN
    # =====================
    with tab1:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            try:

                result = login(
                    username,
                    password
                )

                if result["status"] == "success":

                    st.session_state.user_id = (
                        result["data"]["user_id"]
                    )

                    st.session_state.username = username

                    st.success("Login berhasil")

                    st.rerun()

                else:

                    st.error(
                        "Username atau password salah"
                    )

            except Exception as e:

                st.error(f"API Error: {e}")

    # =====================
    # REGISTER
    # =====================
    with tab2:

        reg_username = st.text_input(
            "Username Baru",
            key="register_username"
        )

        reg_password = st.text_input(
            "Password Baru",
            type="password",
            key="register_password"
        )

        if st.button("Register"):

            try:

                result = register(
                    reg_username,
                    reg_password
                )

                if result["status"] == "success":

                    st.success(
                        "Register berhasil, silakan login"
                    )

                else:

                    st.error("Register gagal")

            except Exception as e:

                st.error(f"API Error: {e}")

    st.stop()

# =====================
# LOAD SESSION
# =====================
if st.session_state.current_session is None:

    result = get_sessions(
        st.session_state.user_id
    )

    sessions = result["data"]

    if not sessions:

        new_session = create_session(
            st.session_state.user_id
        )

        st.session_state.current_session = (
            new_session["session_id"]
        )

    else:

        st.session_state.current_session = (
            sessions[0][0]
        )

# =====================
# LOAD CHAT HISTORY
# =====================
if len(st.session_state.messages) == 0:

    result = load_chat(
        st.session_state.current_session
    )

    st.session_state.messages = (
        result["data"]
    )

# =====================
# SHOW CHAT HISTORY
# =====================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

# =====================
# USER INPUT
# =====================
user_input = st.chat_input(
    "Tulis pesan..."
)

if user_input:

    # =====================
    # SHOW USER MESSAGE
    # =====================
    with st.chat_message("user"):

        st.write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # =====================
    # SAVE USER CHAT
    # =====================
    save_chat(
        st.session_state.current_session,
        "user",
        user_input
    )

    # =====================
    # AI RESPONSE
    # =====================
    with st.chat_message("assistant"):

        result = ai_chat(user_input)

        ai_reply = result["response"]

        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    # =====================
    # SAVE AI CHAT
    # =====================
    save_chat(
        st.session_state.current_session,
        "assistant",
        ai_reply
    )

# =====================
# SIDEBAR
# =====================
with st.sidebar:

    st.title("💬 Sessions")

    st.write(
        f"Login sebagai:\n\n{st.session_state.username}"
    )

    # =====================
    # LOGOUT
    # =====================
    if st.button("🚪 Logout"):

        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.current_session = None
        st.session_state.messages = []

        st.rerun()

    # =====================
    # NEW CHAT
    # =====================
    if st.button("➕ New Chat"):

        result = create_session(
            st.session_state.user_id
        )

        st.session_state.current_session = (
            result["session_id"]
        )

        st.session_state.messages = []

        st.rerun()

    # =====================
    # CLEAR CHAT
    # =====================
    if st.button("🧹 Clear Chat"):

        clear_chat(
            st.session_state.current_session
        )

        st.session_state.messages = []

        st.rerun()

    st.divider()

    # =====================
    # SESSION LIST
    # =====================
    result = get_sessions(
        st.session_state.user_id
    )

    sessions = result["data"]

    for s in sessions:

        session_id = s[0]
        title = s[1]

        col1, col2 = st.columns([4, 1])

        # =====================
        # OPEN SESSION
        # =====================
        with col1:

            if st.button(
                f"📌 {title}",
                key=f"session_{session_id}"
            ):

                st.session_state.current_session = (
                    session_id
                )

                result = load_chat(
                    session_id
                )

                st.session_state.messages = (
                    result["data"]
                )

                st.rerun()

        # =====================
        # DELETE SESSION
        # =====================
        with col2:

            if st.button(
                "❌",
                key=f"delete_{session_id}"
            ):

                delete_session(
                    session_id,
                    st.session_state.user_id
                )

                st.session_state.messages = []

                result = get_sessions(
                    st.session_state.user_id
                )

                sessions = result["data"]

                if sessions:

                    st.session_state.current_session = (
                        sessions[0][0]
                    )

                else:

                    new_session = create_session(
                        st.session_state.user_id
                    )

                    st.session_state.current_session = (
                        new_session["session_id"]
                    )

                st.rerun()