import streamlit as st

st.set_page_config(page_title="StudyBuddy", layout="wide")

st.title("🧠 StudyBuddy")

st.markdown("""
Welcome to your **AI Study Operating System** 🚀

Use the sidebar to navigate:
- 📊 Dashboard
- 📅 Tasks
- 📝 Notes
- 🤖 AI Chat
- 🎯 Exam Tracker
""")

import streamlit as st
import time
from utils_ultra import add_xp, update_streak, set_multiplier

# ---------------- TIMER STATE ----------------
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "end_time" not in st.session_state:
    st.session_state.end_time = None


# ---------------- SIDEBAR UI ----------------
st.sidebar.title("⏰ Focus Timer")

minutes = st.sidebar.number_input("Minutes", 0, 180, 0)
seconds = st.sidebar.number_input("Seconds", 0, 59, 30)

start = st.sidebar.button("▶️ Start Focus")
stop = st.sidebar.button("⛔ Stop Timer")

timer_display = st.sidebar.empty()


# ---------------- START TIMER ----------------
if start:
    total_seconds = minutes * 60 + seconds

    if total_seconds > 0:
        st.session_state.timer_running = True
        st.session_state.end_time = time.time() + total_seconds

        set_multiplier(2)  # 🔥 XP boost active
        st.sidebar.success("Focus Mode Activated (2x XP) 🔥")


# ---------------- STOP TIMER ----------------
if stop:
    st.session_state.timer_running = False
    st.session_state.end_time = None

    set_multiplier(1)
    st.sidebar.warning("Focus Mode stopped")


# ---------------- LIVE TIMER ----------------
if st.session_state.timer_running and st.session_state.end_time:

    remaining = int(st.session_state.end_time - time.time())

    if remaining > 0:
        mins = remaining // 60
        secs = remaining % 60

        timer_display.markdown(f"### ⏳ {mins:02d}:{secs:02d}")

        time.sleep(1)
        st.rerun()

    else:
        # ---------------- TIMER DONE ----------------
        st.session_state.timer_running = False
        st.session_state.end_time = None

        set_multiplier(1)

        add_xp(50)          # 🎯 reward
        update_streak()     # 🔥 streak boost

        timer_display.markdown("### 🎉 DONE!")
        st.sidebar.success("Focus Complete! +50 XP 🔥")