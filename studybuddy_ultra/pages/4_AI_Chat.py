import streamlit as st
from utils_ai import ask_ai

st.title("🤖 AI Study Chat")

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.form("chat_form", clear_on_submit=True):
    msg = st.text_input("Ask AI")
    send = st.form_submit_button("Send")

if send and msg:
    st.session_state.chat.append(("You", msg))
    reply = ask_ai(msg)
    st.session_state.chat.append(("AI", reply))

for role, text in st.session_state.chat:
    st.write(f"{role}: {text}")
