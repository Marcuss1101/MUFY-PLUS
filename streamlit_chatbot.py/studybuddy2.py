import streamlit as st
from datetime import datetime, date, timedelta
import random
import json

# OPTIONAL: GenAI (OpenAI)
try:
    from openai import OpenAI
    client = OpenAI(api_key=st.secrets.get(""))
    
    AI_ENABLED = True
except:
    AI_ENABLED = False


# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="StudyHub AI", layout="wide")


# ----------------------------
# SESSION STATE
# ----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "subjects" not in st.session_state:
    st.session_state.subjects = ["General"]

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "last_active" not in st.session_state:
    st.session_state.last_active = None

if "exams" not in st.session_state:
    st.session_state.exams = []


# ----------------------------
# AI HELPERS
# ----------------------------
def ai_generate(prompt):
    """Call GenAI if available, else fallback."""
    if not AI_ENABLED:
        return "⚠️ AI not enabled. Add OPENAI_API_KEY."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI error: {str(e)}"


def ai_quote():
    prompt = "Give a short motivational study quote (max 15 words)."
    return ai_generate(prompt)


def ai_study_plan(tasks, exams):
    prompt = f"""
    You are a study coach.

    Tasks:
    {json.dumps(tasks, default=str)}

    Exams:
    {json.dumps(exams, default=str)}

    Create a simple prioritized study plan for today in bullet points.
    Keep it short and actionable.
    """
    return ai_generate(prompt)


def ai_suggest_next_task(tasks):
    prompt = f"""
    Based on these tasks:
    {tasks}

    What should the student study next? Give 1 recommendation only.
    """
    return ai_generate(prompt)


def ai_summarize_notes(notes):
    prompt = f"""
    Summarize these study notes into clean bullet points:

    {notes}
    """
    return ai_generate(prompt)


# ----------------------------
# STREAK SYSTEM
# ----------------------------
def update_streak():
    today = date.today()
    last = st.session_state.last_active

    if last is None:
        st.session_state.streak = 1
    else:
        diff = (today - last).days
        if diff == 1:
            st.session_state.streak += 1
        elif diff > 1:
            st.session_state.streak = 1

    st.session_state.last_active = today


# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("🧠 StudyHub AI")

st.sidebar.subheader("🔥 Streak")
st.sidebar.metric("Days", st.session_state.streak)

if st.sidebar.button("Mark Today Studied"):
    update_streak()

st.sidebar.divider()

st.sidebar.subheader("💬 AI Quote of the Day")
st.sidebar.write(ai_quote())

st.sidebar.divider()

st.sidebar.subheader("🧠 AI Study Helper")
if st.sidebar.button("What should I study next?"):
    st.sidebar.info(ai_suggest_next_task(st.session_state.tasks))

st.sidebar.divider()

st.sidebar.subheader("📊 AI Study Plan")
if st.sidebar.button("Generate Study Plan"):
    st.sidebar.success(ai_study_plan(st.session_state.tasks, st.session_state.exams))


# ----------------------------
# MAIN UI
# ----------------------------
st.title("📚 StudyHub AI Dashboard")

col1, col2 = st.columns(2)


# ----------------------------
# SUBJECTS
# ----------------------------
with col1:
    st.subheader("📘 Subjects")

    new_subject = st.text_input("Add subject")
    if st.button("Add Subject"):
        if new_subject and new_subject not in st.session_state.subjects:
            st.session_state.subjects.append(new_subject)

    st.write(st.session_state.subjects)


# ----------------------------
# TASKS
# ----------------------------
with col2:
    st.subheader("📌 Add Task")

    task_title = st.text_input("Task title")
    subject = st.selectbox("Subject", st.session_state.subjects)
    deadline = st.date_input("Deadline")

    if st.button("Add Task"):
        if task_title:
            st.session_state.tasks.append({
                "title": task_title,
                "subject": subject,
                "deadline": deadline,
                "done": False
            })


st.subheader("📋 Tasks")

for i, task in enumerate(st.session_state.tasks):
    colA, colB, colC, colD = st.columns([3, 2, 2, 1])

    with colA:
        st.write(task["title"])

    with colB:
        st.write(task["subject"])

    with colC:
        days_left = (task["deadline"] - date.today()).days
        st.write(f"{days_left} days left")

    with colD:
        if st.button("✔", key=f"done_{i}"):
            st.session_state.tasks[i]["done"] = True

    if task["done"]:
        st.success("Completed")


# ----------------------------
# EXAMS
# ----------------------------
st.subheader("📆 Exam Countdown")

exam_name = st.text_input("Exam name")
exam_date = st.date_input("Exam date", key="exam")

if st.button("Add Exam"):
    if exam_name:
        st.session_state.exams.append({
            "name": exam_name,
            "date": exam_date
        })

for exam in st.session_state.exams:
    days = (exam["date"] - date.today()).days
    st.write(f"{exam['name']} → {days} days left")


# ----------------------------
# NOTES + AI SUMMARY
# ----------------------------
st.subheader("📝 Notes")

st.session_state.notes = st.text_area("Write your notes here...", st.session_state.notes)

if st.button("Summarize Notes (AI)"):
    st.info(ai_summarize_notes(st.session_state.notes))


# ----------------------------
# FOOTER INSIGHT
# ----------------------------
st.subheader("🧠 Smart Insight")

if st.button("Analyze My Study Progress"):
    prompt = f"""
    Tasks: {st.session_state.tasks}
    Exams: {st.session_state.exams}

    Give a short analysis of study progress and improvement tips.
    """
    st.success(ai_generate(prompt))


st.caption("StudyHub AI — powered learning assistant 🚀")