import streamlit as st
from services.api_client import (
    login,
    register
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

                    st.error("Username atau password salah")

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
# MAIN APP
# =====================
st.success(
    f"Selamat datang, {st.session_state.username}"
)

st.write("Backend API berhasil terhubung 🚀")

# =====================
# CHAT UI SEMENTARA
# =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# tampilkan chat
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

# input user
user_input = st.chat_input(
    "Tulis pesan..."
)

if user_input:

    # tampilkan user
    with st.chat_message("user"):

        st.write(user_input)

    # simpan memory
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # dummy AI response
    ai_reply = (
        f"AI menerima pesan: {user_input}"
    )

    with st.chat_message("assistant"):

        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

# =====================
# SIDEBAR
# =====================
with st.sidebar:

    st.title("⚙ Menu")

    st.write(
        f"Login sebagai:\n\n{st.session_state.username}"
    )

    if st.button("🚪 Logout"):

        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.messages = []

        st.rerun()

    if st.button("🧹 Clear Chat"):

        st.session_state.messages = []

        st.rerun()