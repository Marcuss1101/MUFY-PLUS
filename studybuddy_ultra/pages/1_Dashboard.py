import streamlit as st
import json

from utils_ai_quiz import generate_ai_quiz
from utils_ultra import add_xp, update_streak


st.title("🎮 AI Quizizz Dashboard")


# ---------------- STEP 2: LOAD AI QUIZ ----------------
if "quiz" not in st.session_state:

    raw = generate_ai_quiz()

    try:
        data = json.loads(raw)
        quiz = data["quiz"]
    except:
        st.error("❌ AI returned invalid quiz format")
        st.stop()

    st.session_state.quiz = quiz
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.xp_awarded = []


quiz = st.session_state.quiz


# ---------------- SAFETY CHECK ----------------
if not quiz or len(quiz) == 0:
    st.error("❌ Quiz is empty")
    st.stop()


# ---------------- FINISHED SCREEN ----------------
if st.session_state.finished:

    st.success("🎉 Quiz Completed!")

    total = len(quiz)
    score = st.session_state.score

    st.metric("Score", f"{score} / {total}")

    # 🔥 XP SYSTEM
    base_xp = score * 20
    bonus_xp = 0

    if score == total:
        bonus_xp = 50
        st.balloons()
        st.success("🔥 Perfect Score +50 XP!")

    total_xp = base_xp + bonus_xp

    add_xp(total_xp)
    update_streak()

    st.info(f"⭐ XP Earned: {total_xp}")

    if st.button("🔁 Restart Quiz"):
        # regenerate fresh quiz
        raw = generate_ai_quiz()

        try:
            data = json.loads(raw)
            quiz = data["quiz"]
        except:
            st.error("AI failed again")
            st.stop()

        st.session_state.quiz = quiz
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.finished = False
        st.session_state.xp_awarded = []

    st.stop()


# ---------------- CURRENT QUESTION ----------------
q = quiz[st.session_state.index]

st.subheader(f"Q{st.session_state.index + 1}: {q['question']}")

options = q["options"][:4]

choice = st.radio(
    "Choose answer:",
    options,
    key=f"q_{st.session_state.index}"
)


# ---------------- NEXT BUTTON ----------------
if st.button("Next Question"):

    correct = q["answer"]

    # CHECK ANSWER
    if choice == correct:
        st.session_state.score += 1
        add_xp(10)
        st.success("✅ Correct +10 XP")
    else:
        st.error(f"❌ Wrong! Correct answer: {correct}")

    # MOVE NEXT
    st.session_state.index += 1

    # FINISH CHECK
    if st.session_state.index >= len(quiz):
        st.session_state.finished = True

    st.rerun()